import datetime
from typing import Any

from fastapi import Depends
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.models import User
from src.database import get_async_session

from src.auth.db import CustomUserDatabase


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield CustomUserDatabase(session, User)


def map_to_datetime(obj: dict[str, Any]) -> dict[str, Any]:
    def str_to_datetime(ts: str) -> datetime.datetime:
        return datetime.datetime.fromisoformat(ts)

    for k, v in obj.items():
        if "date" in k:
            obj[k] = str_to_datetime(v)
            break

    return obj
