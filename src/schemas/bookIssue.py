from pydantic import BaseModel, EmailStr, validator
from typing import Optional, List
from datetime import datetime, date, timedelta


class BookIssueCreate(BaseModel):
    book_id: int
    student_id: int
    issue_date: Optional[date] = None
    due_date: Optional[date] = None


class BookReturn(BaseModel):
    issue_id: int
    return_date: Optional[date] = None
