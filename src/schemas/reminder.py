from dataclasses import dataclass
from pydantic import BaseModel, EmailStr, validator, field_validator
from typing import Optional, List
from datetime import datetime, date
import re


@dataclass
class ReminderRecord:
    id: Optional[int] = None
    student_id: int = None
    book_issue_id: int = None
    reminder_type: str = None
    sent_date: date = None
    days_before_due: int = None
    created_at: datetime = None


# default email configurationn usinig smtp server is given below. provide the sender email and password for authentication.
# without valid credentials it will throw an error - Bad Credentials
@dataclass
class EmailConfig:
    smtp_server: str = "smtp.gmail.com"
    smtp_port: int = 587
    sender_email: str = ""
    sender_password: str = ""
    sender_name: str = "Library Management Netenrich"
