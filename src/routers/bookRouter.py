from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from controllers.bookController import BookController
from schemas.book import BookCreate, BookRead, BookUpdate
from config.db import get_db

router = APIRouter()


@router.post("/", response_model=dict, status_code=201)
async def createBook(book_data: BookCreate, db: AsyncSession = Depends(get_db)):
    try:
        new_book = await BookController.createBook(db, book_data)
        return {
            "message": "book created successfully",
            "book": BookRead.model_validate(new_book).model_dump(),
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
