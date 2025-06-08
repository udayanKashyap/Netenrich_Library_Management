from fastapi import FastAPI, APIRouter, BackgroundTasks, HTTPException, Depends
from config.db import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from controllers.overdueTrackingController import (
    EmailController,
    OverdueTrackingController,
    ScheduleController,
)
from schemas.reminder import EmailConfig
from contextlib import asynccontextmanager

router = APIRouter()


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        # provide the sender email and password for authentication.
        # without valid credentials it will throw an error - Bad Credentials
        email_config = EmailConfig(
            smtp_server="smtp.gmail.com",
            smtp_port=587,
            sender_email="",
            sender_password="",
            sender_name="Library Management Netenrich",
        )

        # initialize services
        email_service = EmailController(email_config)
        tracking_service = OverdueTrackingController(email_service, get_db)
        await tracking_service.init()
        scheduler_service = ScheduleController(tracking_service)

        # start the scheduler
        scheduler_service.setup_scheduler()
        scheduler_service.start()

        app.state.email_service = email_service
        app.state.tracking_service = tracking_service
        app.state.scheduler_service = scheduler_service

        print("Overdue tracking system started successfully")
        print("Email reminders will be sent daily at 12:00 AM")

    except Exception as e:
        print(f"Failed to initialize tracking system: {str(e)}")

    yield

    print("Shutting down Library Management System")
    try:
        if hasattr(app.state, "scheduler_service"):
            app.state.scheduler_service.stop()
        print("Overdue tracking system stopped ")
    except Exception as e:
        print(f"Error during shutdown: {str(e)}")


# manually send reminders for testing
@router.post("/send-reminders")
async def trigger_manual_reminders(background_tasks: BackgroundTasks):
    try:
        from main import app

        if not hasattr(app.state, "tracking_service"):
            raise HTTPException(
                status_code=503, detail="Overdue tracking service is not available"
            )

        tracking_service = app.state.tracking_service

        background_tasks.add_task(tracking_service.process_reminders)

        return {
            "message": "Manual reminder processing started, reminders will be processed in the background",
        }

    except Exception as e:
        print(f"Error triggering manual reminders: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Failed to trigger reminders: {str(e)}"
        )
