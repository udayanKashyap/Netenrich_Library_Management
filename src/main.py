from fastapi import FastAPI
from routers.bookRouter import router as bookRouter
from routers.studentRouter import router as studentRouter
from routers.bookIssueRouter import router as bookIssueRouter
from routers.overdueRouter import router as overdueRouter
from routers.overdueRouter import lifespan
from routers.aiRouter import router as aiRouter

app = FastAPI(lifespan=lifespan)

app.include_router(bookRouter, prefix="/books", tags=["Books"])
app.include_router(studentRouter, prefix="/students", tags=["Student"])
app.include_router(bookIssueRouter, prefix="/book-issue", tags=["Book Management"])
app.include_router(overdueRouter, prefix="/overdue", tags=["Overdue Management"])
app.include_router(aiRouter, prefix="/ai", tags=["AI Assistant"])


@app.get("/")
def read_root():
    return {"Library Management System is running"}
