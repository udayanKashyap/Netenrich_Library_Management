from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from controllers.studentController import StudentController
from schemas.book import BookCreate, BookRead, BookUpdate
from schemas.student import StudentCreate, StudentRead
from config.db import get_db
from typing import Optional

router = APIRouter()


@router.post("/", response_model=dict, status_code=201)
async def create_student(
    student_data: StudentCreate, db: AsyncSession = Depends(get_db)
):
    try:
        new_student = await StudentController.createStudent(db, student_data)
        return {
            "message": "student created successfully",
            "student": StudentRead.model_validate(new_student).model_dump(),
        }

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/search", response_model=dict)
async def search_students(
    department: Optional[str] = Query(None, description="Filter by department"),
    semester: Optional[int] = Query(None, description="Filter by semester"),
    name: Optional[str] = Query(None, description="Filter by name (partial match)"),
    roll_number: Optional[str] = Query(
        None, description="Filter by roll number (partial match)"
    ),
    phone: Optional[str] = Query(
        None, description="Filter by phone number (partial match)"
    ),
    db: AsyncSession = Depends(get_db),
):
    try:
        students = await StudentController.searchStudents(
            db,
            department=department,
            semester=semester,
            name=name,
            roll_number=roll_number,
            phone=phone,
        )

        return {
            "message": "Search completed successfully",
            "students": [
                StudentRead.model_validate(student).model_dump() for student in students
            ],
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
