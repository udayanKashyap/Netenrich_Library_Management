from fastapi import FastAPI
from routers.bookRouter import router as bookRouter
from routers.studentRouter import router as studentRouter
from routers.bookIssueRouter import router as bookIssueRouter

app = FastAPI()

app.include_router(bookRouter, prefix="/books", tags=["Books"])
app.include_router(studentRouter, prefix="/students", tags=["Student"])
app.include_router(bookIssueRouter, prefix="/book-issue", tags=["Book Management"])


@app.get("/")
def read_root():
    return {"Library Management System is running"}
