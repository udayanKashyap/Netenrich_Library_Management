import os
import json
import asyncio
from typing import AsyncGenerator, Optional, Dict, Any, List
from datetime import datetime, date

from google import genai
from google.genai import types
from fastapi import HTTPException
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from config.db import get_db

DATABASE_SCHEMA = """
Database Schema:
1. Books table:
   - id (integer, primary key)
   - title (string, indexed)
   - isbn (string, unique)
   - number_of_copies (integer)
   - author (string, indexed)
   - category (string, indexed)
   - created_at (datetime)
   - updated_at (datetime)

2. Students table:
   - id (integer, primary key)
   - name (string, indexed)
   - roll_number (string, unique, indexed)
   - department (string, indexed)
   - semester (integer)
   - phone (string)
   - email (string, unique)
   - created_at (datetime)
   - updated_at (datetime)

3. BookIssues table:
   - id (integer, primary key)
   - book_id (foreign key to Books.id)
   - student_id (foreign key to Students.id)
   - issue_date (date)
   - due_date (date)
   - return_date (date, nullable)
   - created_at (datetime)
   - updated_at (datetime)

4. ReminderHistory table:
   - id (integer, primary key)
   - student_id (foreign key to Students.id)
   - book_issue_id (foreign key to BookIssues.id)
   - reminder_type (string)
   - sent_date (date)
   - days_before_due (integer)
   - created_at (datetime)

Table names: "Books", "Students", "BookIssues", "ReminderHistory"
"""

GEMINI_PROMPT = f"""
You are a SQL query generator for a library management system. Convert natural language questions to PostgreSQL queries.
And DO NOT ANSWER questions outside the context and scope of this system and schema.

{DATABASE_SCHEMA}

Rules:
1. Always use double quotes for table names: "Books", "Students", "BookIssues", "ReminderHistory"
2. Use proper PostgreSQL syntax
3. For date comparisons, use CURRENT_DATE
4. Return only the SQL query, no explanations
5. Use JOINs when querying across tables
6. For overdue books: return_date IS NULL AND due_date < CURRENT_DATE
7. Use LIMIT when appropriate to avoid huge results
8. Use aggregate functions (COUNT, SUM, AVG) when asking for totals or statistics

Examples:
Q: "How many books are currently issued?"
A: SELECT COUNT(*) FROM "BookIssues" WHERE return_date IS NULL;

Q: "Show overdue books with student details"
A: SELECT s.name, s.roll_number, b.title, bi.due_date, (CURRENT_DATE - bi.due_date) as days_overdue FROM "BookIssues" bi JOIN "Students" s ON bi.student_id = s.id JOIN "Books" b ON bi.book_id = b.id WHERE bi.return_date IS NULL AND bi.due_date < CURRENT_DATE ORDER BY bi.due_date;

Q: "Books by author Shakespeare"
A: SELECT * FROM "Books" WHERE LOWER(author) LIKE LOWER('%shakespeare%');

Convert this question to SQL:
"""


class AIController:
    @staticmethod
    async def generate_sql_query(question: str) -> str:
        try:
            client = genai.Client(api_key="AIzaSyD-CcfVwDnR8OQkytOVfEJesAKWdaMgl3I")

            response = client.models.generate_content(
                model="gemini-2.5-flash-preview-05-20",
                config=types.GenerateContentConfig(system_instruction=GEMINI_PROMPT),
                contents=question,
            )
            sql_query = response.text.strip()

            if sql_query.startswith("```sql"):
                sql_query = sql_query.replace("```sql", "").replace("```", "").strip()
            elif sql_query.startswith("```"):
                sql_query = sql_query.replace("```", "").strip()

            return sql_query
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Error generating SQL: {str(e)}"
            )

    @staticmethod
    async def execute_sql_query(query: str) -> List[Dict[str, Any]]:
        try:
            async for session in get_db():
                result = await session.execute(text(query))
                rows = result.fetchall()
                columns = result.keys()

                return [
                    {column: row[i] for i, column in enumerate(columns)} for row in rows
                ]
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    @staticmethod
    def serialize_result(obj):
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        raise TypeError(f"Object of type {type(obj)} is not JSON serializable")

    @staticmethod
    async def stream_response(question: str) -> AsyncGenerator[str, None]:
        """Stream the response with results only (no SQL query display)"""
        try:
            yield (
                json.dumps({"type": "status", "content": "Processing your request..."})
                + "\n"
            )
            sql_query = await AIController.generate_sql_query(question)

            yield json.dumps({"type": "status", "content": "Fetching data..."}) + "\n"
            results = await AIController.execute_sql_query(sql_query)

            yield (
                json.dumps(
                    {
                        "type": "data",
                        "content": {"total_rows": len(results)},
                    }
                )
                + "\n"
            )

            chunk_size = 10
            for i in range(0, len(results), chunk_size):
                chunk = results[i : i + chunk_size]
                yield (
                    json.dumps(
                        {"type": "data_chunk", "content": chunk},
                        default=AIController.serialize_result,
                    )
                    + "\n"
                )

            yield (
                json.dumps(
                    {
                        "type": "complete",
                        "content": {
                            "message": f"Query completed successfully. Returned {len(results)} rows.",
                            "total_rows": len(results),
                        },
                    }
                )
                + "\n"
            )
        except Exception as e:
            yield json.dumps({"type": "error", "content": str(e)}) + "\n"
