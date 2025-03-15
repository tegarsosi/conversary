from fastapi import APIRouter, HTTPException
from backend.models import ConversationEntry
from backend.services.llm import llm_service
from datetime import date
from tortoise.exceptions import DoesNotExist
from pydantic import BaseModel

router = APIRouter()


class ConversationRequest(BaseModel):
    user_message: str


class ConversationResponse(BaseModel):
    id: int
    user_message: str
    ai_response: str
    date: date


@router.post("/conversations/", response_model=ConversationResponse)
async def save_conversation(
    convo: ConversationRequest
) -> ConversationResponse:
    """Save a new conversation entry

    param convo: The conversation request
    return: The conversation response
    """
    # Get recent conversation history for context
    today = date.today()
    recent_conversations = await ConversationEntry.filter(
        date=today
    ).order_by('-id').limit(10).all()

    history = [
        {"user": c.user_message, "ai": c.ai_response}
        for c in reversed(recent_conversations)
    ]

    # Get AI response with context
    ai_response = await llm_service.get_ai_response(
        convo.user_message,
        conversation_history=history
    )

    entry = await ConversationEntry.create(
        date=today,
        user_message=convo.user_message,
        ai_response=ai_response
    )
    return ConversationResponse(
        id=entry.id,
        user_message=convo.user_message,
        ai_response=ai_response,
        date=entry.date
    )


@router.get("/conversations/{entry_date}")
async def get_conversation(
    entry_date: str
) -> list[ConversationResponse]:
    """Get conversation for a specific date

    param entry_date: The date of the conversation
    return: The conversation response
    """
    try:
        conversations = await ConversationEntry.filter(date=entry_date).all()
        return [
            {
                "id": convo.id,
                "user_message": convo.user_message,
                "ai_response": convo.ai_response,
                "date": convo.date
            }
            for convo in conversations
        ]
    except DoesNotExist:
        raise HTTPException(
            status_code=404, detail="No conversation found for the given date"
        )


@router.get("/conversations/")
async def get_all_conversations() -> list[ConversationResponse]:
    """Get all conversation entries

    return: The conversation response
    """
    conversations = await ConversationEntry.all()
    return [
        {
            "id": convo.id,
            "user_message": convo.user_message,
            "ai_response": convo.ai_response,
            "date": convo.date
        }
        for convo in conversations
    ]
