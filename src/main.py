from fastapi import FastAPI
import uvicorn
from src.polls.router import router_polls, router_questions, router_choices, router_votes
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


# if __name__ == '__main__':
#     uvicorn.run(app)
