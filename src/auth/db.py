from typing import Optional
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy import select

from src.auth.schemas import UserRead


class CustomUserDatabase(SQLAlchemyUserDatabase):
	"""
	Extend the SQLAlchemyUserDatabase to add custom methods.
	"""

	def __init__(self, session, user_table) -> None:
		super().__init__(session, user_table)

	async def get_by_username(self, username: str) -> Optional[UserRead]:
		query = select(self.user_table).where(self.user_table.username == username)
		result = await self.session.execute(query)
		user = result.scalars().first()
		return user
