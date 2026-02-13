from fastapi import FastAPI
from app.models import create_db_and_tables
from contextlib import asynccontextmanager
from app.routes import routes
from app.users import auth_backend, fastapi_users
from app.schemas import UserCreate,UserRead,UserUpdate

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(routes)
app.include_router(fastapi_users.get_auth_router(auth_backend),prefix="/auth/jwt",tags=["auth"])
app.include_router(fastapi_users.get_register_router(UserRead, UserCreate), prefix="/auth",tags=["auth"])
app.include_router(fastapi_users.get_reset_password_router(), prefix="/auth",tags=["auth"])
app.include_router(fastapi_users.get_verify_router(UserRead), prefix="/auth", tags = ["users"])
app.include_router(fastapi_users.get_users_router(UserRead, UserUpdate),prefix="/users",tags=["users"])