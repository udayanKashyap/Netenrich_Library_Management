from typing import Optional
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from controllers.aiController import AIController
from schemas.ai import QuestionRequest

router = APIRouter()


@router.post("/ask")
async def ask_question(request: QuestionRequest):
    """
    Webhook endpoint that accepts natural language questions about the library database
    and returns streaming responses with SQL queries and results.
    """
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")

    return StreamingResponse(
        AIController.stream_response(request.question),
        media_type="application/x-ndjson",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",  # For nginx
        },
    )
