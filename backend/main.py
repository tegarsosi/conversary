from fastapi import FastAPI
from backend.database import init_db
from backend.api import conversations, summaries

app = FastAPI(title="Conversary")


@app.on_event("startup")
async def startup():
    await init_db()

# Register API routers
app.include_router(conversations.router)
app.include_router(summaries.router)
