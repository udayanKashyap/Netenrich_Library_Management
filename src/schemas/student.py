from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional, List
from datetime import datetime
import re


class StudentCreate(BaseModel):
    name: str
    roll_number: str
    department: str
    semester: int
    phone: str
    email: EmailStr

    @field_validator("name")
    @classmethod
    def validate_name(cls, v):
        if not v or not v.strip():
            raise ValueError("Name cannot be empty")
        if len(v.strip()) < 2:
            raise ValueError("Name must be at least 2 characters long")
        if len(v.strip()) > 255:
            raise ValueError("Name cannot exceed 255 characters")
        return v.strip().title()

    @field_validator("roll_number")
    @classmethod
    def validate_roll_number(cls, v):
        if not v or not v.strip():
            raise ValueError("Roll number cannot be empty")
        if len(v.strip()) < 3:
            raise ValueError("Roll number must be at least 3 characters long")
        if len(v.strip()) > 50:
            raise ValueError("Roll number cannot exceed 50 characters")
        return v.strip().upper()

    @field_validator("department")
    @classmethod
    def validate_department(cls, v):
        if not v or not v.strip():
            raise ValueError("Department cannot be empty")

        return v.strip()

    @field_validator("semester")
    @classmethod
    def validate_semester(cls, v):
        if v is None:
            raise ValueError("Semester cannot be None")
        if v < 1:
            raise ValueError("Semester cannot be lower than 1")
        return v

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, v):
        if not v or not v.strip():
            raise ValueError("Phone number cannot be empty")

        phone_digits = re.sub(r"\D", "", v)

        if len(phone_digits) == 10:
            if not re.match(r"^[6-9]\d{9}$", phone_digits):
                raise ValueError("Invalid phone number format")
        else:
            raise ValueError("Phone number must be 10 digits")

        return phone_digits

    @field_validator("email")
    @classmethod
    def validate_email(cls, v):
        if not v or not str(v).strip():
            raise ValueError("Email cannot be empty")
        email_str = str(v).strip().lower()

        if len(email_str) > 254:
            raise ValueError("Email address is too long")

        return email_str


class StudentRead(BaseModel):
    name: str
    roll_number: str
    department: str
    semester: int
    phone: str
    email: EmailStr
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
