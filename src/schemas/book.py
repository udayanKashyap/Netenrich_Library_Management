from pydantic import BaseModel, EmailStr, validator, field_validator
from typing import Optional, List
from datetime import datetime
import re


class BookCreate(BaseModel):
    title: str
    isbn: str
    number_of_copies: int
    author: str
    category: str

    @field_validator("title")
    @classmethod
    def validate_title(cls, v):
        if not v or not v.strip():
            raise ValueError("Title cannot be empty")
        if len(v.strip()) < 2:
            raise ValueError("Title must be at least 2 characters long")
        if len(v.strip()) > 255:
            raise ValueError("Title cannot exceed 255 characters")
        return v.strip()

    @field_validator("isbn")
    @classmethod
    def validate_isbn(cls, v):
        if not v or not v.strip():
            raise ValueError("ISBN cannot be empty")

        isbn_clean = re.sub(r"[-\s]", "", v.strip())

        if len(isbn_clean) == 10:
            if not re.match(r"^\d{9}[\dX]$", isbn_clean):
                raise ValueError("Invalid ISBN-10 format")
        elif len(isbn_clean) == 13:
            if not re.match(r"^\d{13}$", isbn_clean):
                raise ValueError("Invalid ISBN-13 format")
        else:
            raise ValueError("ISBN must be either 10 or 13 digits")

        return v.strip()

    @field_validator("number_of_copies")
    @classmethod
    def validate_number_of_copies(cls, v):
        if v is None:
            raise ValueError("Number of copies cannot be None")
        if v < 0:
            raise ValueError("Number of copies cannot be negative")
        return v

    @field_validator("author")
    @classmethod
    def validate_author(cls, v):
        if not v or not v.strip():
            raise ValueError("Author cannot be empty")
        if len(v.strip()) < 2:
            raise ValueError("Author name must be at least 2 characters long")
        if len(v.strip()) > 255:
            raise ValueError("Author name cannot exceed 255 characters")
        return v.strip()

    @field_validator("category")
    @classmethod
    def validate_category(cls, v):
        if v is not None:
            if not v.strip():
                raise ValueError("Category cannot be empty")
            if len(v.strip()) < 2:
                raise ValueError("Category must be at least 2 characters long")
            if len(v.strip()) > 255:
                raise ValueError("Category cannot exceed 255 characters")

            return v.strip()
        return v


class BookUpdate(BaseModel):
    title: Optional[str] = None
    isbn: Optional[str] = None
    number_of_copies: Optional[int] = None
    author: Optional[str] = None
    category: Optional[str] = None

    @field_validator("title")
    @classmethod
    def validate_title(cls, v):
        if v is not None:
            if not v.strip():
                raise ValueError("Title cannot be empty")
            if len(v.strip()) < 2:
                raise ValueError("Title must be at least 2 characters long")
            if len(v.strip()) > 255:
                raise ValueError("Title cannot exceed 255 characters")
            return v.strip()
        return v

    @field_validator("isbn")
    @classmethod
    def validate_isbn(cls, v):
        if v is not None:
            if not v.strip():
                raise ValueError("ISBN cannot be empty")

            isbn_clean = re.sub(r"[-\s]", "", v.strip())

            if len(isbn_clean) == 10:
                if not re.match(r"^\d{9}[\dX]$", isbn_clean):
                    raise ValueError("Invalid ISBN-10 format")
            elif len(isbn_clean) == 13:
                if not re.match(r"^\d{13}$", isbn_clean):
                    raise ValueError("Invalid ISBN-13 format")
            else:
                raise ValueError("ISBN must be either 10 or 13 digits")

            return v.strip()
        return v

    @field_validator("number_of_copies")
    @classmethod
    def validate_number_of_copies(cls, v):
        if v is not None:
            if v < 0:
                raise ValueError("Number of copies cannot be negative")
        return v

    @field_validator("author")
    @classmethod
    def validate_author(cls, v):
        if v is not None:
            if not v.strip():
                raise ValueError("Author cannot be empty")
            if len(v.strip()) < 2:
                raise ValueError("Author name must be at least 2 characters long")
            if len(v.strip()) > 255:
                raise ValueError("Author name cannot exceed 255 characters")
            return v.strip()
        return v


class BookRead(BaseModel):
    id: int
    title: str
    isbn: str
    author: str
    category: str
    number_of_copies: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
