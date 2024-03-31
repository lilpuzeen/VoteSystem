from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.polls.utils import get_current_active_user

import src.polls.question.models as model
import src.polls.question.schemas as schema
from src.polls.question.action import question_action


router_questions = APIRouter(
    prefix="/questions",
    tags=["Questions"],
    dependencies=[Depends(get_current_active_user)]
)


@router_questions.post("/{poll_id}", dependencies=[Depends(get_current_active_user)])
async def create_question(
        poll_id: int,
        new_question: schema.CreateQuestion,
        session: AsyncSession = Depends(get_async_session)
):
    new_question_instance = model.Question(
        poll_id=poll_id,
        question_text=new_question.question_text
    )

    return await question_action.create(db=session, obj_in=new_question_instance)


@router_questions.put("/{question_id}", dependencies=[Depends(get_current_active_user)])
async def update_question(
        updated_question: schema.UpdateQuestion,
        question_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    db_obj = await question_action.get(db=session, id=question_id)

    return await question_action.update(db=session, db_obj=db_obj, obj_in=updated_question)


@router_questions.delete("/{question_id}", dependencies=[Depends(get_current_active_user)])
async def delete_question(
        question_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    return await question_action.remove(db=session, id=question_id)


@router_questions.get("/{question_id}", dependencies=[Depends(get_current_active_user)])
async def get_question(
        question_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    return await question_action.get(db=session, id=question_id)