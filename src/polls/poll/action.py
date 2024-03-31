from typing import Optional

from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import selectinload

from src.database import get_async_session

import src.polls.poll.schemas as schema
import src.polls.poll.models as models
from src.polls.question.models import Question

from src.actions.actions import BaseActions, ModelType


class PollActions(BaseActions[models.Poll, schema.CreatePoll, schema.UpdatePoll]):
    """Poll actions with basic CRUD operations"""

    async def get(self,
                  id: int,
                  db: AsyncSession = Depends(get_async_session)) -> Optional[ModelType]:
        async with db as session:
            query = (
                select(self.model)
                .filter(self.model.id == id)
                .options(
                    selectinload(models.Poll.questions)
                    .selectinload(Question.choices)
                )
            )
            result = await session.execute(query)
            obj = result.scalars().first()
            if obj:
                obj_data = jsonable_encoder(obj)

                for question in obj_data["questions"]:
                    question.pop("poll_id", None)
                return obj_data
            else:
                raise HTTPException(status_code=404, detail=f"Object with ID {id} not found.")

    async def get_all(self, *, skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_async_session)) -> list[ModelType]:
        async with db as session:
            query = (
                select(self.model)
                .options(
                    selectinload(models.Poll.questions)
                    .selectinload(Question.choices)
                )
            )
            result = await session.execute(query)
            obj = result.scalars().all()
            if obj:
                obj_data = jsonable_encoder(obj)
                for poll in obj_data:
                    for question in poll["questions"]:
                        question.pop("poll_id", None)
                return obj_data
            else:
                raise HTTPException(status_code=404, detail=f"Objects not found.")


poll_action = PollActions(models.Poll)
