from fastapi import Depends

from src.auth.base_config import fastapi_users
from src.auth.models import User


async def get_current_active_user(
		current_user: User = Depends(fastapi_users.current_user(active=True))):
    return current_user
