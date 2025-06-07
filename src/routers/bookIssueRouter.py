from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from controllers.bookIssueController import BookIssueController
from schemas.bookIssue import BookIssueRequest, BookReturnRequest, BookIssueResponse
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
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
