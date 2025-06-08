from datetime import timedelta, date
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from sqlalchemy import and_, select
import smtplib
import asyncio
from typing import AsyncGenerator, List, Callable

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from models.models import BookIssue, ReminderHistory
from schemas.reminder import EmailConfig, ReminderRecord
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


# email controller (create, send, etc)
class EmailController:
    def __init__(self, config: EmailConfig):
        self.config = config

    async def sendEmail(self, to_email: str, subject: str, body: str) -> bool:
        def _send_sync():
            try:
                msg = MIMEMultipart()
                msg["From"] = f"{self.config.sender_name} <{self.config.sender_email}>"
                msg["To"] = to_email
                msg["Subject"] = subject

                msg.attach(MIMEText(body, "html"))

                with smtplib.SMTP(
                    self.config.smtp_server, self.config.smtp_port
                ) as server:
                    server.starttls()
                    server.login(self.config.sender_email, self.config.sender_password)
                    server.send_message(msg)

                return True

            except Exception as e:
                raise Exception(f"Failed to send email to {to_email}: {str(e)}")

        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(None, _send_sync)

        if result:
            print(f"Email sent to {to_email}")
        return result


# overdue functions controller
# functions name describe their functions
class OverdueTrackingController:
    def __init__(
        self,
        email_service: EmailController,
        db_session_factory: Callable[[], AsyncGenerator[AsyncSession, None]],
    ):
        self.email_service = email_service
        self.db_session_factory = db_session_factory
        self.reminder_history: List[ReminderRecord] = []

    async def init(self):
        async for db in self.db_session_factory():
            try:
                result = await db.execute(select(ReminderHistory))
                self.reminder_history = result.scalars().all()
            except Exception as e:
                await db.rollback()
                raise e

    async def get_books_needing_reminders(self, db: AsyncSession) -> List:
        today = date.today()
        reminder_start_date = today + timedelta(days=5)

        query = (
            select(BookIssue)
            .where(
                and_(
                    BookIssue.return_date.is_(None),
                    BookIssue.due_date <= reminder_start_date,
                )
            )
            .options(selectinload(BookIssue.student), selectinload(BookIssue.book))
        )
        result = await db.execute(query)
        issues = result.scalars().all()

        return issues

    # check for unsent reminders
    async def should_send_reminder(
        self, issue, reminder_type: str, db: AsyncSession
    ) -> bool:
        today = date.today()

        query = select(ReminderHistory).where(
            and_(
                ReminderHistory.book_issue_id == issue.id,
                ReminderHistory.reminder_type == reminder_type,
                ReminderHistory.sent_date == today,
            )
        )
        result = await db.execute(query)
        existing_reminder = result.scalar_one_or_none()
        return existing_reminder is None

    # store sent reminders
    async def record_reminder_sent(
        self, issue, reminder_type: str, days_before_due: int, db: AsyncSession
    ):
        reminder_record = ReminderHistory(
            student_id=issue.student_id,
            book_issue_id=issue.id,
            reminder_type=reminder_type,
            sent_date=date.today(),
            days_before_due=days_before_due,
        )
        db.add(reminder_record)
        await db.commit()

        print(f"Recorded reminder: {reminder_type} for issue {issue.id}")

    # process reminders
    async def process_reminders(self):
        async for db in self.db_session_factory():
            try:
                issues = await self.get_books_needing_reminders(db)

                for issue in issues:
                    await self.process_single_issue(issue, db)

                print(f"sent {len(issues)} issues.")
                break

            except Exception as e:
                print(f"Error: {str(e)}")
                await db.rollback()
                raise

    # process single reminder
    async def process_single_issue(self, issue, db: AsyncSession):
        today = date.today()
        days_until_due = (issue.due_date - today).days

        student = issue.student
        book = issue.book

        if days_until_due >= 0:
            if days_until_due <= 5 and await self.should_send_reminder(
                issue, "pre_due", db
            ):
                subject, body = self.create_pre_due_reminder(
                    student.name, book.title, issue.due_date, days_until_due
                )

                if await self.email_service.sendEmail(student.email, subject, body):
                    await self.record_reminder_sent(
                        issue, "pre_due", days_until_due, db
                    )

        else:
            days_overdue = abs(days_until_due)
            if await self.should_send_reminder(issue, "overdue", db):
                subject, body = self.create_overdue_reminder(
                    student.name, book.title, issue.due_date, days_overdue
                )

                if await self.email_service.sendEmail(student.email, subject, body):
                    await self.record_reminder_sent(
                        issue, "overdue", days_until_due, db
                    )

    # email boilerplates
    def create_pre_due_reminder(
        self, student_name: str, book_title: str, due_date: date, days_remaining: int
    ) -> tuple[str, str]:
        subject = f"Library Reminder: Book Due in {days_remaining} Days"

        body = f"""
        <html>
        <body>
            <h2>Library Book Reminder</h2>
            <p>Dear {student_name},</p>
            
            <p>This is a friendly reminder that you have a book due soon:</p>
            
            <div style="background-color: #f0f8ff; padding: 15px; border-left: 4px solid #007bff;">
                <strong>Book:</strong> {book_title}<br>
                <strong>Due Date:</strong> {due_date.strftime('%B %d, %Y')}<br>
                <strong>Days Remaining:</strong> {days_remaining}
            </div>
            
            <p>Please return the book on or before the due date to avoid late fees.</p>
            
            <p>Thank you,<br>
            University Library Team</p>
        </body>
        </html>
        """

        return subject, body

    def create_overdue_reminder(
        self, student_name: str, book_title: str, due_date: date, days_overdue: int
    ) -> tuple[str, str]:
        subject = f"URGENT: Overdue Book - {days_overdue} Days Late"

        body = f"""
        <html>
        <body>
            <h2 style="color: #dc3545;">Overdue Book Notice</h2>
            <p>Dear {student_name},</p>
            
            <p><strong>Your book is now overdue. Please return it immediately.</strong></p>
            
            <div style="background-color: #fff3cd; padding: 15px; border-left: 4px solid #ffc107;">
                <strong>Book:</strong> {book_title}<br>
                <strong>Due Date:</strong> {due_date.strftime('%B %d, %Y')}<br>
                <strong>Days Overdue:</strong> {days_overdue}
            </div>
            
            <p>Please return the book to the library circulation desk as soon as possible.</p>
            
            <p>University Library Team</p>
        </body>
        </html>
        """

        return subject, body


# email schedule service controller
class ScheduleController:
    def __init__(self, tracking_service: OverdueTrackingController):
        self.scheduler = AsyncIOScheduler()
        self.tracking_service = tracking_service

    def setup_scheduler(self):
        self.scheduler.add_job(
            self.tracking_service.process_reminders,
            CronTrigger(hour=0, minute=0),
            id="daily_reminder_check",
            replace_existing=True,
        )

    def start(self):
        self.scheduler.start()

    def stop(self):
        self.scheduler.shutdown()
