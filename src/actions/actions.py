from typing import Any, Generic, Optional, Type, TypeVar, cast

from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import selectinload

from src.database import Base, get_async_session
from src.auth.utils import map_to_datetime

import src.polls.schemas as schema
import src.polls.models as models

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class BaseActions(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        Base class that can be extended by other action classes.
           Provides basic CRUD and listing operations.

        :param model: The SQLAlchemy model
        :type model: Type[ModelType]
        """
        self.model = model

    async def get_all(
        self, *, skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_async_session)
    ) -> list[ModelType]:
        async with db as session:
            query = select(self.model).offset(skip).limit(limit)
            result = await session.execute(query)
            return cast(list[ModelType], result.scalars().all())

    async def get(self, id: int, db: AsyncSession = Depends(get_async_session)) -> Optional[ModelType]:
        async with db as session:
            query = select(self.model).filter(self.model.id == id)
            result = await session.execute(query)
            obj = result.scalars().first()
            if obj:
                return obj
            else:
                raise HTTPException(status_code=404, detail=f"Object with ID {id} not found.")

    async def create(self, *, obj_in: CreateSchemaType, db: AsyncSession = Depends(get_async_session)) -> ModelType:
        obj_in_data = map_to_datetime(jsonable_encoder(obj_in))
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update(
            self,
            *,
            db_obj: ModelType,
            obj_in: UpdateSchemaType | dict[str, Any],
            db: AsyncSession = Depends(get_async_session)
    ) -> ModelType:
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])

        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def remove(self, *, id: int, db: AsyncSession = Depends(get_async_session)) -> ModelType:
        query = select(self.model).where(self.model.id == id)
        result = await db.execute(query)
        obj = result.scalars().first()
        if obj:
            await db.delete(obj)
            await db.commit()
            return obj
        else:
            raise HTTPException(status_code=404, detail=f"Object with ID {id} not found.")


# TODO: Implement actions for other models
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
                    .selectinload(models.Question.choices)
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
                    .selectinload(models.Question.choices)
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


class QuestionActions(BaseActions[models.Question, schema.CreateQuestion, schema.CreateQuestion]):
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


class ChoiceActions(BaseActions[models.Choice, schema.CreateChoice, schema.UpdateChoice]):
    """Choice actions with basic CRUD operations"""

    pass


class VoteActions(BaseActions[models.Vote, schema.CreateVote, schema.UpdateVote]):
    """Vote actions with basic CRUD operations"""

    pass


poll_action = PollActions(models.Poll)
question_action = QuestionActions(models.Question)
choice_action = QuestionActions(models.Choice)
vote_action = QuestionActions(models.Vote)
