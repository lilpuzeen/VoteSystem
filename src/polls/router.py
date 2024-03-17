import pytz

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.models import User
from src.auth.base_config import fastapi_users
from src.auth.schemas import UserRead

from src.database import get_async_session

from src.actions.actions import poll_action, question_action, choice_action, vote_action

import src.polls.models as model
import src.polls.schemas as schema

router_polls = APIRouter(
	prefix="/polls",
	tags=["Polls"]
)

router_questions = APIRouter(
    prefix="/questions",
    tags=["Polls"]
)

router_choices = APIRouter(
    prefix="/choices",
    tags=["Polls"]
)

router_votes = APIRouter(
    prefix="/votes",
    tags=["Polls"]
)


async def get_current_active_user(
		current_user: User = Depends(fastapi_users.current_user(active=True))):
    return current_user


@router_polls.post("")
async def create_poll(
        new_poll: schema.CreatePoll,
        session: AsyncSession = Depends(get_async_session),
        current_user: UserRead = Depends(get_current_active_user)
):
    created_by_id = current_user.id
    if new_poll.end_date.tzinfo is not None:
        new_poll.end_date = new_poll.end_date.astimezone(pytz.utc).replace(tzinfo=None)

    new_poll_instance = model.Poll(
        title=new_poll.title,
        description=new_poll.description,
        created_by=created_by_id,
        end_date=new_poll.end_date,
    )

    return await poll_action.create(db=session, obj_in=new_poll_instance)


@router_polls.get("/{poll_id}")
async def get_poll(poll_id: int, session: AsyncSession = Depends(get_async_session)):
    return await poll_action.get_poll_with_questions(db=session, id=poll_id)


@router_questions.post("/{poll_id}")
async def create_question(
        poll_id: int,
        new_question: schema.CreateQuestion,
        session: AsyncSession = Depends(get_async_session),
        current_user: UserRead = Depends(get_current_active_user)
):
    new_question_instance = model.Question(
        poll_id=poll_id,
        question_text=new_question.question_text
    )

    return await question_action.create(db=session, obj_in=new_question_instance)


@router_questions.get("/{question_id}")
async def get_question(question_id: int, session: AsyncSession = Depends(get_async_session)):
    return await question_action.get_question_with_choices(db=session, id=question_id)


@router_choices.post("/{question_id}")
async def create_choice(
        question_id: int,
        new_choice: schema.CreateChoice,
        session: AsyncSession = Depends(get_async_session),
        current_user: UserRead = Depends(get_current_active_user)
):
    new_choice_instance = model.Choice(
        question_id=question_id,
        choice_text=new_choice.choice_text
    )

    return await choice_action.create(db=session, obj_in=new_choice_instance)


# TODO: handle multiple votes from the same user on the same choice
@router_votes.post("/{choice_id}")
async def create_vote(
        choice_id: int,
        new_vote: schema.CreateVote,
        session: AsyncSession = Depends(get_async_session),
        current_user: UserRead = Depends(get_current_active_user)
):
    new_vote_instance = model.Vote(
        choice_id=choice_id,
        user_id=current_user.id,
        vote_timestamp=new_vote.vote_ts
    )

    return await vote_action.create(db=session, obj_in=new_vote_instance)
