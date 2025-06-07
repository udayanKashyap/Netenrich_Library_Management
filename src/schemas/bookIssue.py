from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import datetime, date, timedelta
from .student import StudentRead
from .book import BookRead


class BookIssueRequest(BaseModel):
    book_id: int
    student_id: int
    issue_date: Optional[date] = None
    due_date: Optional[date] = None

    @field_validator("issue_date", mode="before")
    @classmethod
    def set_issue_date(cls, value):
        return value or date.today()

    @field_validator("due_date", mode="after")
    @classmethod
    def set_due_date(cls, value, info):
        issue_date = info.data.get("issue_date")
        if value is not None:
            return value
        if issue_date is None:
            issue_date = date.today()
        return issue_date + timedelta(days=30)


class BookReturnRequest(BaseModel):
    issue_id: int
    return_date: Optional[date] = None

    @field_validator("return_date", mode="before")
    @classmethod
    def set_return_date(cls, value):
        return value or date.today()


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
