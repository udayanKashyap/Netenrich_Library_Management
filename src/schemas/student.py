from pydantic import BaseModel, EmailStr, validator
from typing import Optional, List


class StudentCreate(BaseModel):
    name: str
    roll_number: str
    department: str
    semester: int
    phone: str
    email: EmailStr
