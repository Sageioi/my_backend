import uuid
from typing import Optional
from fastapi import Depends, Request, FastAPI

from fastapi_users import FastAPIUsers,BaseUserManager, UUIDIDMixin, models
from fastapi_users.authentication import (AuthenticationBackend, JWTStrategy, BearerTransport)
from fastapi_users.db import SQLAlchemyUserDatabase, SQLAlchemyBaseUserTableUUID
from sqlalchemy.orm import DeclarativeBase, relationship
from app.models import User, get_user_db


SECRET = "User_password1234"

class UserManager(UUIDIDMixin, BaseUserManager[User,uuid.UUID]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    async def on_after_register(
        self, user: User, request: Optional[Request] = None):
        print(f"User {user.id} has registered")

    async def on_after_forgot_password(self, user: User, token: str, request: Optional[Request] = None):
        print(f"User {user.id} has forgot password. Reset token: {token}")

    async def on_after_request_verify(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"Verification for user {user.id} has been requested. Verification token: {token}")

async def get_user_manager(user_db: SQLAlchemyUserDatabase = Depends(get_user_db)):
    return UserManager(user_db)

bearer_transport = BearerTransport(tokenUrl="auth/jwt/token")
def get_jwt_strategy():
    return JWTStrategy(secret=SECRET,lifetime_seconds=3600)