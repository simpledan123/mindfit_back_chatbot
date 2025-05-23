from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from schemas.chat import ChatRequest, ChatResponse
from services.chatbot_chain import generate_chat_response
from core.dependencies import get_db, get_current_user
from models.user import User

router = APIRouter()

@router.post("/", response_model=ChatResponse)
async def chat_endpoint(
    request: ChatRequest,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    return generate_chat_response(user=user, message=request.message, db=db)
