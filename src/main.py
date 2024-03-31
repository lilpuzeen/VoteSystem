from fastapi import FastAPI

from src.polls.image.router import router_images
from src.polls.poll.router import router_polls
from src.polls.question.router import router_questions
from src.polls.choice.router import router_choices
from src.polls.vote.router import router_votes

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
app.include_router(router_questions)
app.include_router(router_choices)
app.include_router(router_votes)
app.include_router(router_images)
