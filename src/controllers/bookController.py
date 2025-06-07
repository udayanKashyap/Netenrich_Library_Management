from sqlalchemy import create_engine, delete, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.book import BookCreate, BookUpdate
from models.models import Book
from typing import Optional, List


class BookController:
    @staticmethod
    async def getBookById(db: AsyncSession, book_id: int) -> Optional[Book]:
        try:
            result = await db.execute(select(Book).where(Book.id == book_id))
            print(f"\n{book_id}\n")
            print(result)
            return result.scalar_one_or_none()
        except Exception as e:
            raise Exception(f"Error fetching book: {str(e)}")

    @staticmethod
    async def createBook(db: AsyncSession, book_data: BookCreate) -> Book:
        """Create new book"""
        try:
            new_book = Book(
                title=book_data.title,
                isbn=book_data.isbn,
                number_of_copies=book_data.number_of_copies,
                author=book_data.author,
                category=book_data.category,
            )
            print(new_book)

            db.add(new_book)
            await db.commit()
            return new_book
        except Exception as e:
            await db.rollback()
            raise Exception(f"Error Creating book: {str(e)}")

    @staticmethod
    async def updateBook(
        db: AsyncSession, book_id: int, book_update: BookUpdate
    ) -> Optional[Book]:
        try:
            existing_book = await BookController.getBookById(db, book_id)
            if not existing_book:
                return None

            update_data = {
                nonNullFields: field
                for nonNullFields, field in book_update.dict().items()
                if field is not None
            }
            if not update_data:
                return existing_book

            await db.execute(
                update(Book).where(Book.id == book_id).values(**update_data)
            )
            await db.commit()

            return await BookController.getBookById(db, book_id)
        except Exception as e:
            await db.rollback()
            raise Exception(f"Error Updating Book: {str(e)}")

    @staticmethod
    async def delete_book(db: AsyncSession, book_id: int) -> bool:
        try:
            existing_book = await BookController.getBookById(db, book_id)
            if not existing_book:
                return False

            await db.execute(delete(Book).where(Book.id == book_id))
            await db.commit()

            return True
        except Exception as e:
            await db.rollback()
            raise Exception(f"Error Updating Book: {str(e)}")
