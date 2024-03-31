import pytz

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.schemas import UserRead
from src.database import get_async_session
from src.polls.utils import get_current_active_user

from src.polls.poll.action import poll_action
import src.polls.poll.models as model
import src.polls.poll.schemas as schema

router_polls = APIRouter(
	prefix="/polls",
	tags=["Polls"]
)


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
    return await poll_action.get(db=session, id=poll_id)


@router_polls.get("")
async def get_all_polls(session: AsyncSession = Depends(get_async_session)):
    return await poll_action.get_all(db=session)


@router_polls.put("/{poll_id}", dependencies=[Depends(get_current_active_user)])
async def update_poll(
        updated_poll: schema.UpdatePoll,
        poll_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    if updated_poll.end_date.tzinfo is not None:
        updated_poll.end_date = updated_poll.end_date.astimezone(pytz.utc).replace(tzinfo=None)

    db_obj = await poll_action.get(db=session, id=poll_id)

    return await poll_action.update(db=session, db_obj=db_obj, obj_in=updated_poll)


@router_polls.delete("/{poll_id}", dependencies=[Depends(get_current_active_user)])
async def delete_poll(
        poll_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    return await poll_action.remove(db=session, id=poll_id)