from fastapi import APIRouter, HTTPException
from backend.models import DailySummary
from datetime import date
from tortoise.exceptions import DoesNotExist
from pydantic import BaseModel

router = APIRouter()


class SummaryRequest(BaseModel):
    summary_text: str
    sentiment_score: float | None = None
    notes: str | None = None


@router.post("/summaries/")
async def create_summary(summary: SummaryRequest):
    """ Create a new daily summary """
    entry = await DailySummary.create(
        date=date.today(),
        summary_text=summary.summary_text,
        sentiment_score=summary.sentiment_score,
        notes=summary.notes
    )
    return {"message": "Summary created successfully", "id": entry.id}


@router.get("/summaries/{entry_date}")
async def get_summary(entry_date: str):
    """ Get summary for a specific date """
    try:
        summary = await DailySummary.get(date=entry_date)
        return {
            "id": summary.id,
            "date": summary.date,
            "summary_text": summary.summary_text,
            "sentiment_score": summary.sentiment_score,
            "notes": summary.notes
        }
    except DoesNotExist:
        raise HTTPException(
            status_code=404,
            detail="No summary found for the given date"
        )
