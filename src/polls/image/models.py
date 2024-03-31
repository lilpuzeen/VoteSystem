from sqlalchemy import Column, Integer, String

from src.database import Base


class Image(Base):
	__tablename__ = "image"

	id = Column("id", Integer, primary_key=True)
	name = Column("name", String, nullable=False, unique=True)
