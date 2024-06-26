from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import (Boolean, Column, Integer,
                        String)
from sqlalchemy.orm import relationship

from src.database import Base


class User(SQLAlchemyBaseUserTable[int], Base):
	__tablename__ = "user"

	id = Column(Integer, primary_key=True)
	username = Column(String, nullable=False, unique=True)
	email = Column(String, nullable=False, unique=True)
	hashed_password: str = Column(String(length=1024), nullable=False)
	is_active: bool = Column(Boolean, default=True, nullable=False)
	is_superuser: bool = Column(Boolean, default=False, nullable=False)
	is_verified: bool = Column(Boolean, default=False, nullable=False)

	polls = relationship("Poll", back_populates="users")
	votes = relationship("Vote", back_populates="user")
