from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Date, null
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime, date

Base = declarative_base()


class Book(Base):
    __tablename__ = "Books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, index=True)
    isbn = Column(String(13), unique=True, nullable=False)
    number_of_copies = Column(Integer, nullable=False, default=0)
    author = Column(String(255), nullable=False, index=True)
    category = Column(String(255), nullable=False, index=True)

    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    issues = relationship("BookIssue", back_populates="book")

    def __repr__(self) -> str:
        return f"Book: title:{self.title}, isbn:{self.isbn}, copies:{self.number_of_copies}"


class Student(Base):
    __tablename__ = "Students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    roll_number = Column(String(50), nullable=False, index=True, unique=True)
    department = Column(String(255), nullable=False, index=True)
    semester = Column(Integer, nullable=False)
    phone = Column(String(10), nullable=False)
    email = Column(String(255), unique=True, nullable=False)

    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    issues = relationship("BookIssue", back_populates="student")

    def __repr__(self) -> str:
        return f"Student: name:{self.name}, roll:{self.roll_number}"


class BookIssue(Base):
    __tablename__ = "BookIssues"

    id = Column(Integer, primary_key=True, index=True)

    book_id = Column(Integer, ForeignKey("Books.id"), nullable=False)
    student_id = Column(Integer, ForeignKey("Students.id"), nullable=False)

    issue_date = Column(Date, nullable=False, default=date.today)
    due_date = Column(Date, nullable=False)
    return_date = Column(Date, nullable=True)

    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    book = relationship("Book", back_populates="issues")
    student = relationship("Student", back_populates="issues")

    @property
    def is_overdue(self):
        if self.return_date is None and self.due_date < date.today():
            return True
        return False

    def __str__(self) -> str:
        return f"Student: name:{self.student_id}, book:{self.book_id}, issued:{self.issue_date}"


class ReminderHistory(Base):
    __tablename__ = "ReminderHistory"

    id = Column(Integer, primary_key=True, index=True)

    student_id = Column(Integer, ForeignKey("Students.id"), nullable=False)
    book_issue_id = Column(Integer, ForeignKey("BookIssues.id"), nullable=False)

    reminder_type = Column(String(50), nullable=False)
    sent_date = Column(Date, nullable=False, default=date.today)
    days_before_due = Column(Integer, nullable=False)

    created_at = Column(DateTime, default=datetime.now)
