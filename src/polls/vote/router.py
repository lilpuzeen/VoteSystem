import pytz

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.schemas import UserRead
from src.database import get_async_session
from src.polls.utils import get_current_active_user

import src.polls.vote.models as model
import src.polls.vote.schemas as schema

from src.polls.vote.action import vote_action

router_votes = APIRouter(
    prefix="/votes",
    tags=["Votes"]
)


# TODO: handle multiple votes from the same user on the same choice
@router_votes.post("/{choice_id}", dependencies=[Depends(get_current_active_user)])
async def create_vote(
        choice_id: int,
        new_vote: schema.CreateVote,
        session: AsyncSession = Depends(get_async_session),
        current_user: UserRead = Depends(get_current_active_user)
):
    if new_vote.vote_ts.tzinfo is not None:
        new_vote.vote_ts = new_vote.vote_ts.astimezone(pytz.utc).replace(tzinfo=None)

    new_vote_instance = model.Vote(
        choice_id=choice_id,
        user_id=current_user.id,
        vote_timestamp=new_vote.vote_ts
    )

    return await vote_action.create(db=session, obj_in=new_vote_instance)


@router_votes.delete("/{vote_id}", dependencies=[Depends(get_current_active_user)])
async def delete_vote(vote_id: int, session: AsyncSession = Depends(get_async_session)):
    return await vote_action.remove(db=session, id=vote_id)
