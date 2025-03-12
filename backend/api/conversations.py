from fastapi import APIRouter, HTTPException
from backend.models import ConversationEntry
from datetime import date
from tortoise.exceptions import DoesNotExist
from pydantic import BaseModel

router = APIRouter()


class ConversationRequest(BaseModel):
    user_message: str
    ai_response: str


@router.post("/conversations/")
async def save_conversation(convo: ConversationRequest):
    """ Save a new conversation entry """
    entry = await ConversationEntry.create(
        date=date.today(),
        user_message=convo.user_message,
        ai_response=convo.ai_response
    )
    return {"message": "Conversation saved successfully", "id": entry.id}


@router.get("/conversations/{entry_date}")
async def get_conversation(entry_date: str):
    """ Get conversation for a specific date """
    try:
        conversations = await ConversationEntry.filter(date=entry_date).all()
        return [
            {
                "id": convo.id,
                "user_message": convo.user_message,
                "ai_response": convo.ai_response
            }
            for convo in conversations
        ]
    except DoesNotExist:
        raise HTTPException(
            status_code=404, detail="No conversation found for the given date"
        )
