from typing import Optional

from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from fastapi import Depends, HTTPException
from fastapi.encoders import jsonable_encoder

from src.database import get_async_session

import src.polls.question.models as models
import src.polls.question.schemas as schema
from src.actions.actions import BaseActions, ModelType


class QuestionActions(BaseActions[models.Question, schema.CreateQuestion, schema.UpdateQuestion]):
    """Question actions with basic CRUD operations"""

    async def get(self, id: int, db: AsyncSession = Depends(get_async_session)) -> Optional[ModelType]:
        async with db as session:
            query = (
                select(self.model)
                .filter(self.model.id == id)
                .options(
                    selectinload(models.Question.choices)
                )
            )
            result = await session.execute(query)
            obj = result.scalars().first()
            if obj:
                obj_data = jsonable_encoder(obj)
                question_data = obj_data
                question_data.pop("poll_id", None)
                return question_data
            else:
                raise HTTPException(status_code=404, detail=f"Object with ID {id} not found.")


question_action = QuestionActions(models.Question)