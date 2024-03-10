from fastapi import FastAPI
from src.polls.router import router as router_polls
from src.auth.base_config import fastapi_users, auth_backend
from src.auth.schemas import UserCreate, UserRead

app = FastAPI(
    title="Voting System"
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth",
    tags=["Auth"]
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["Auth"]
)

app.include_router(router_polls)
