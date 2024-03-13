from typing import Optional

from fastapi import Depends, Request
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_users import (BaseUserManager, IntegerIDMixin, exceptions, models,
                           schemas)
from fastapi_users.db import BaseUserDatabase

from src.auth.db import CustomUserDatabase
from src.auth.models import User
from src.auth.utils import get_user_db
from src.config import SECRET_AUTH


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    reset_password_token_secret = SECRET_AUTH
    verification_token_secret = SECRET_AUTH

    def __init__(self, user_db: BaseUserDatabase, *args, **kwargs):
        super().__init__(user_db, *args, **kwargs)

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        # TODO: add email confirmation
        print(f"User {user.username} has registered.")

    async def authenticate(
        self,
        credentials: OAuth2PasswordRequestForm
    ) -> Optional[User]:
        user = None
        if "@" in credentials.username:
            user = await self.user_db.get_by_email(credentials.username)
        else:
            user = await self.user_db.get_by_username(credentials.username)

        if user is None:
            self.password_helper.hash(credentials.password)
            return None

        verified, updated_password_hash = self.password_helper.verify_and_update(
            credentials.password, user.hashed_password
        )
        if not verified:
            return None

        if updated_password_hash is not None:
            await self.user_db.update(user, {"hashed_password": updated_password_hash})

        return user

    async def create(
        self,
        user_create: schemas.UC,
        safe: bool = False,
        request: Optional[Request] = None,
    ) -> models.UP:
        await self.validate_password(user_create.password, user_create)

        existing_user = await self.user_db.get_by_email(user_create.email)
        if existing_user is not None:
            raise exceptions.UserAlreadyExists()

        user_dict = (
            user_create.create_update_dict()
            if safe
            else user_create.create_update_dict_superuser()
        )
        password = user_dict.pop("password")
        user_dict["hashed_password"] = self.password_helper.hash(password)

        created_user = await self.user_db.create(user_dict)

        await self.on_after_register(created_user, request)

        return created_user


async def get_user_manager(user_db: CustomUserDatabase = Depends(get_user_db)) -> UserManager:
    yield UserManager(user_db)
