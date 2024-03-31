from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship

from src.database import Base

import datetime


class Poll(Base):
	__tablename__ = "poll"

	id = Column("id", Integer, primary_key=True)
	title = Column("title", String, nullable=False, unique=True)
	description = Column("description", String)
	created_by = Column("created_by", Integer, ForeignKey("user.id"), nullable=False)
	start_date = Column("start_date", TIMESTAMP, default=datetime.datetime.now())
	end_date = Column("end_date", TIMESTAMP, nullable=False)

	questions = relationship("Question", back_populates="poll")
	users = relationship("User", back_populates="polls")