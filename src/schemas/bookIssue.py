from pydantic import BaseModel, field_validator, model_validator
from typing import Optional
from datetime import datetime, date, timedelta
from .student import StudentRead
from .book import BookRead


class BookIssueRequest(BaseModel):
    book_id: int
    student_id: int
    issue_date: Optional[date] = None
    due_date: Optional[date] = None

    @field_validator("book_id")
    @classmethod
    def validate_book_id(cls, v):
        if v is None or v <= 0:
            raise ValueError("Book ID must be a positive integer")
        return v

    @field_validator("student_id")
    @classmethod
    def validate_student_id(cls, v):
        if v is None or v <= 0:
            raise ValueError("Student ID must be a positive integer")
        return v

    @model_validator(mode="before")
    @classmethod
    def set_dates(cls, data: dict):
        # issue date
        issue_date = data.get("issue_date")
        if issue_date is None:
            issue_date = date.today()

        # due date
        due_date = data.get("due_date")
        if due_date is None:
            due_date = issue_date + timedelta(days=30)

        if due_date <= issue_date:
            raise ValueError("Due date must be after issue date")

        data["issue_date"] = issue_date
        data["due_date"] = due_date
        return data


class BookReturnRequest(BaseModel):
    issue_id: int
    return_date: Optional[date] = None

    @field_validator("issue_id")
    @classmethod
    def validate_issue_id(cls, v):
        if v is None:
            raise ValueError("Issue ID cannot be None")
        if v <= 0:
            raise ValueError("Issue ID must be a positive integer")
        return v

    @field_validator("return_date", mode="before")
    @classmethod
    def set_return_date(cls, v):
        if v is None:
            return date.today()

        return v


class BookIssueResponse(BaseModel):
    id: int
    book_id: int
    student_id: int
    issue_date: date
    due_date: date
    return_date: Optional[date]
    is_overdue: bool
    book: BookRead
    student: StudentRead

    model_config = {"from_attributes": True}
