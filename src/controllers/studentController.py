from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.student import StudentCreate
from models.models import Student
from typing import Optional, List


class StudentController:
    @staticmethod
    async def getStudentById(db: AsyncSession, student_id: int) -> Optional[Student]:
        try:
            result = await db.execute(select(Student).where(Student.id == student_id))
            return result.scalar_one_or_none()
        except Exception as e:
            raise Exception(f"Error fetching book: {str(e)}")

    @staticmethod
    async def createStudent(db: AsyncSession, student_data: StudentCreate) -> Student:
        try:
            new_student = Student(
                name=student_data.name,
                roll_number=student_data.roll_number,
                department=student_data.department,
                semester=student_data.semester,
                phone=student_data.phone,
                email=student_data.email,
            )
            db.add(new_student)
            await db.commit()
            return new_student

        except Exception as e:
            await db.rollback()
            raise Exception(f"Error Creating student: {str(e)}")

    @staticmethod
    async def searchStudents(
        db: AsyncSession,
        department: Optional[str] = None,
        semester: Optional[int] = None,
        name: Optional[str] = None,
        roll_number: Optional[str] = None,
        phone: Optional[str] = None,
    ) -> List[Student]:
        try:
            query = select(Student)

            if department:
                filter = Student.department == department
                query = query.where(filter)
            if semester:
                filter = Student.semester == semester
                query = query.where(filter)
            if name:
                filter = Student.name.ilike(f"%{name}%")
                query = query.where(filter)
            if roll_number:
                filter = Student.name.ilike(f"%{roll_number}%")
                query = query.where(filter)
            if phone:
                filter = Student.name.ilike(f"%{phone}%")
                query = query.where(filter)

            result = await db.execute(query)
            students = result.scalars().all()

            return students

        except Exception as e:
            raise Exception(f"Error searching students: {str(e)}")
