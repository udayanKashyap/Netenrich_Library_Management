from pydantic import BaseModel, EmailStr, validator
from typing import Optional, List
from datetime import datetime


class StudentCreate(BaseModel):
    name: str
    roll_number: str
    department: str
    semester: int
    phone: str
    email: EmailStr


class StudentRead(BaseModel):
    name: str
    roll_number: str
    department: str
    semester: int
    phone: str
    email: EmailStr
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True  # Replaces orm_mode in v2
    }
