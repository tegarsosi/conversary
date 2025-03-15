from fastapi import FastAPI
from backend.database import init_db
from backend.api import conversations, summaries
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await init_db()
    yield
    # Shutdown
    pass


app = FastAPI(title="Conversary", lifespan=lifespan)

# Register API routers
app.include_router(conversations.router)
app.include_router(summaries.router)
