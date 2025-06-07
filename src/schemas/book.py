from pydantic import BaseModel, EmailStr, validator
from typing import Optional, List
from datetime import datetime


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


class BookRead(BaseModel):
    id: int
    title: str
    isbn: str
    author: str
    category: str
    number_of_copies: int
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True  # Replaces orm_mode in v2
    }
