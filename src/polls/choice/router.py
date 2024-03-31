from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.polls.utils import get_current_active_user

import src.polls.choice.schemas as schema
import src.polls.choice.models as model
from src.polls.choice.action import choice_action

router_choices = APIRouter(
    prefix="/choices",
    tags=["Choices"],
    dependencies=[Depends(get_current_active_user)]
)


@router_choices.post("/{question_id}", dependencies=[Depends(get_current_active_user)])
async def create_choice(
        question_id: int,
        new_choice: schema.CreateChoice,
        session: AsyncSession = Depends(get_async_session),
):
    new_choice_instance = model.Choice(
        question_id=question_id,
        choice_text=new_choice.choice_text
    )

    return await choice_action.create(db=session, obj_in=new_choice_instance)


@router_choices.put("/{choice_id}", dependencies=[Depends(get_current_active_user)])
async def update_choice(
        updated_choice: schema.UpdateChoice,
        choice_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    db_obj = await choice_action.get(db=session, id=choice_id)

    return await choice_action.update(db=session, db_obj=db_obj, obj_in=updated_choice)


@router_choices.delete("/{choice_id}", dependencies=[Depends(get_current_active_user)])
async def delete_choice(
        choice_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    return await choice_action.remove(db=session, id=choice_id)
