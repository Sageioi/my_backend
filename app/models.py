from collections.abc import AsyncGenerator
from datetime import datetime
import uuid

from fastapi import Depends
from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, relationship
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase, SQLAlchemyBaseUserTableUUID


DATABASE_URL = "sqlite+aiosqlite:///./test.db"

class BaseModel(DeclarativeBase): pass

class User(SQLAlchemyBaseUserTableUUID, BaseModel):
    posts = relationship("Post",back_populates="user")

class Post(BaseModel):
    __tablename__ = "posts"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"),nullable=False)
    caption = Column(Text)
    url  = Column(String)
    file_name = Column(String)
    file_type = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="posts")

engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)
async def create_db_and_tables(status = True):
    if status:
        async with engine.begin() as conn  :
          await conn.run_sync(BaseModel.metadata.create_all)
    else :
        await engine.dispose()
        pass

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session

async def get_user_db (session : AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)
