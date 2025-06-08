from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.book import BookCreate, BookUpdate
from models.models import Book
from typing import List, Optional


# Boook controller
# all function names are descriptive of what they do
class BookController:
    @staticmethod
    async def getBookById(db: AsyncSession, book_id: int) -> Optional[Book]:
        try:
            result = await db.execute(select(Book).where(Book.id == book_id))
            return result.scalar_one_or_none()
        except Exception as e:
            raise Exception(f"Error fetching book: {str(e)}")

    @staticmethod
    async def createBook(db: AsyncSession, book_data: BookCreate) -> Book:
        try:
            new_book = Book(
                title=book_data.title,
                isbn=book_data.isbn,
                number_of_copies=book_data.number_of_copies,
                author=book_data.author,
                category=book_data.category,
            )
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
    async def deleteBook(db: AsyncSession, book_id: int) -> bool:
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

    @staticmethod
    async def searchBooks(
        db: AsyncSession,
        title: Optional[str] = None,
        author: Optional[str] = None,
        category: Optional[str] = None,
        isbn: Optional[str] = None,
        page: int = 1,
        limit: int = 10,
    ) -> tuple[List[Book], int]:
        try:
            query = select(Book)
            count_query = select(Book)

            if title:
                title_filter = Book.title.ilike(f"%{title}%")
                query = query.where(title_filter)
                count_query = count_query.where(title_filter)

            if author:
                author_filter = Book.author.ilike(f"%{author}%")
                query = query.where(author_filter)
                count_query = count_query.where(author_filter)

            if category:
                category_filter = Book.category.ilike(f"%{category}%")
                query = query.where(category_filter)
                count_query = count_query.where(category_filter)

            if isbn:
                isbn_filter = Book.isbn == isbn
                query = query.where(isbn_filter)
                count_query = count_query.where(isbn_filter)

            count_result = await db.execute(count_query)
            total_count = len(count_result.scalars().all())

            offset = (page - 1) * limit
            query = query.offset(offset).limit(limit).order_by(Book.title, Book.id)

            result = await db.execute(query)
            books = result.scalars().all()

            return books, total_count

        except Exception as e:
            raise Exception(f"Error searching books: {str(e)}")
