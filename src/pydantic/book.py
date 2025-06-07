from pydantic import BaseModel, EmailStr, validator
from typing import Optional, List


class BookCreate(BaseModel):
    title: str
    isbn: str
    number_of_copies: int
    author: str
    category: str


class BookUpdate(BaseModel):
    title: Optional[str] = None
    isbn: Optional[str] = None
    number_of_copies: Optional[int] = None
    author: Optional[str] = None
    category: Optional[str] = None
