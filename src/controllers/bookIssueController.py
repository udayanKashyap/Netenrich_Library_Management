from fastapi import HTTPException
from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from schemas.bookIssue import BookIssueRequest, BookReturnRequest, BookIssueResponse
from schemas.book import BookRead
from models.models import BookIssue, Book, Student
from controllers.bookController import BookController
from controllers.studentController import StudentController


class BookIssueController:
    @staticmethod
    async def issueBook(db: AsyncSession, issue_data: BookIssueRequest) -> BookIssue:
        try:
            result = await db.execute(select(Book).where(Book.id == issue_data.book_id))
            book = result.scalar_one_or_none()
            result = await db.execute(
                select(Student).where(Student.id == issue_data.student_id)
            )
            student = result.scalar_one_or_none()
            print(f"\n{book}, {student}\n")
            if not book or not student:
                raise HTTPException(status_code=404, detail="book or student not found")

            if book.number_of_copies <= 0:
                raise HTTPException(
                    status_code=400, detail="no available copies for this book"
                )

            result = await db.execute(
                select(BookIssue).where(
                    BookIssue.book_id == issue_data.book_id,
                    BookIssue.student_id == issue_data.student_id,
                    BookIssue.return_date.is_(None),
                )
            )
            existing_issues = result.scalar_one_or_none()
            if existing_issues:
                raise HTTPException(
                    status_code=400, detail="Student already has this book issued"
                )

            # all checks complete, can now issue book
            new_book_issue = BookIssue(
                book_id=issue_data.book_id,
                student_id=issue_data.student_id,
                issue_date=issue_data.issue_date,
                due_date=issue_data.due_date,
            )
            book.number_of_copies -= 1
            db.add(new_book_issue)
            await db.commit()

            return new_book_issue

        except HTTPException:
            raise
        except Exception as e:
            await db.rollback()
            raise Exception(f"Error Creating book: {str(e)}")

    @staticmethod
    async def returnBook(db: AsyncSession, return_data: BookReturnRequest) -> bool:
        try:
            result = await db.execute(
                select(BookIssue).where(
                    BookIssue.id == return_data.issue_id,
                    BookIssue.return_date.is_(None),
                )
            )
            existing_issue = result.scalar_one_or_none()
            if not existing_issue:
                raise HTTPException(
                    status_code=404, detail="book issue not found or already returned"
                )

            existing_issue.return_date = return_data.return_date
            book = await BookController.getBookById(db, existing_issue.book_id)
            book.number_of_copies += 1

            await db.commit()
            return True

        except HTTPException:
            raise
        except Exception as e:
            await db.rollback()
            raise Exception(f"Error Creating book: {str(e)}")

    @staticmethod
    async def getBooksIssuedToStudent(db: AsyncSession, student_id: int) -> List[Book]:
        try:
            student = await StudentController.getStudentById(db, student_id)
            if not student:
                raise HTTPException(status_code=404, detail="student not found")

            result = await db.execute(
                select(BookIssue.book_id).where(
                    BookIssue.student_id == student_id,
                    BookIssue.return_date.is_(None),
                )
            )
            book_ids = result.scalars().all()

            books_issued = [
                await BookController.getBookById(db, book_id) for book_id in book_ids
            ]

            return books_issued

        except HTTPException:
            raise
        except Exception as e:
            await db.rollback()
            raise Exception(f"Error fetching books issued to student: {str(e)}")
