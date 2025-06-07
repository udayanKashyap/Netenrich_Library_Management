from fastapi import FastAPI
from routers.bookRouter import router as bookRouter

app = FastAPI()

app.include_router(bookRouter, prefix="/books", tags=["Books"])


@app.get("/")
def read_root():
    return {"Library Management System is running"}
