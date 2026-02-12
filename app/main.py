from fastapi import FastAPI
from app.models import create_db_and_tables
from contextlib import asynccontextmanager
from app.routes import routes

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    yield
app = FastAPI(lifespan=lifespan)
app.include_router(routes)