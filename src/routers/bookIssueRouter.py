from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from controllers.bookIssueController import BookIssueController
from schemas.bookIssue import BookIssueRequest, BookReturnRequest, BookIssueResponse
from schemas.book import BookRead
from config.db import get_db
from typing import Optional

router = APIRouter()


@router.post("/", response_model=dict, status_code=201)
async def issue_book(issue_data: BookIssueRequest, db: AsyncSession = Depends(get_db)):
    try:
        new_issue = await BookIssueController.issueBook(db, issue_data)
        return {
            "message": "book issued successfully",
            "book_issued": issue_data.book_id,
            "issued_to_student": issue_data.student_id,
        }

    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/return", response_model=dict, status_code=201)
async def return_book(
    return_data: BookReturnRequest, db: AsyncSession = Depends(get_db)
):
    try:
        new_return = await BookIssueController.returnBook(db, return_data)
        return {
            "message": "book returned successfully",
        }

    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/student/{student_id}", response_model=dict, status_code=201)
async def get_books_issued_to_student(
    student_id: int, db: AsyncSession = Depends(get_db)
):
    try:
        books_issued = await BookIssueController.getBooksIssuedToStudent(db, student_id)
        return {
            "books": [
                BookRead.model_validate(book).model_dump() for book in books_issued
            ]
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
