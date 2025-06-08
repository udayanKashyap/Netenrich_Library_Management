from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from controllers.bookController import BookController
from schemas.book import BookCreate, BookRead, BookUpdate
from config.db import get_db
from typing import Optional

router = APIRouter()


@router.post("/", response_model=dict, status_code=201)
async def create_book(book_data: BookCreate, db: AsyncSession = Depends(get_db)):
    try:
        new_book = await BookController.createBook(db, book_data)
        return {
            "message": "book created successfully",
            "book": BookRead.model_validate(new_book).model_dump(),
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/search", response_model=dict)
async def search_books(
    title: Optional[str] = Query(
        None, description="Filter by book title (partial match)"
    ),
    author: Optional[str] = Query(
        None, description="Filter by author name (partial match)"
    ),
    category: Optional[str] = Query(
        None, description="Filter by book category (partial match)"
    ),
    page: int = Query(1, ge=1, description="Page number (starts from 1)"),
    limit: int = Query(10, ge=1, le=100, description="Number of books per page"),
    db: AsyncSession = Depends(get_db),
):
    try:
        books, total_count = await BookController.searchBooks(
            db, title=title, author=author, category=category, page=page, limit=limit
        )

        total_pages = (total_count + limit - 1) // limit

        return {
            "message": "Search completed successfully",
            "pagination": {
                "current_page": page,
                "per_page": limit,
                "total_items": total_count,
                "total_pages": total_pages,
                "has_next": page < total_pages,
                "has_previous": page > 1,
            },
            "books": [BookRead.model_validate(book).model_dump() for book in books],
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{book_id}", response_model=dict, status_code=200)
async def get_book_by_id(book_id: int, db: AsyncSession = Depends(get_db)):
    try:
        book = await BookController.getBookById(db, book_id)
        if not book:
            raise HTTPException(status_code=404, detail="Book not found")

        return BookRead.model_validate(book).model_dump()

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{book_id}", response_model=dict)
async def update_book(
    book_id: int, book_update: BookUpdate, db: AsyncSession = Depends(get_db)
):
    try:
        updated_book = await BookController.updateBook(db, book_id, book_update)
        if not updated_book:
            raise HTTPException(status_code=404, detail="Book Not Found")

        return {
            "message": "Book updated successfully",
            "book": BookRead.model_validate(updated_book).model_dump(),
        }
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{book_id}", response_model=dict)
async def delete_book(book_id: int, db: AsyncSession = Depends(get_db)):
    try:
        deleted = await BookController.deleteBook(db, book_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Book not found")

        return {"message": "book deleted successfully", "book_id": book_id}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
