from tortoise.models import Model
from tortoise import fields
from datetime import date


class ConversationEntry(Model):
    id = fields.IntField(pk=True)
    date = fields.DateField(default=date.today)
    user_message = fields.TextField()
    ai_response = fields.TextField()


class DailySummary(Model):
    id = fields.IntField(pk=True)
    date = fields.DateField(unique=True, default=date.today)
    summary_text = fields.TextField()
    sentiment_score = fields.FloatField(null=True)
    notes = fields.TextField(null=True)
