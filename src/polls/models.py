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


class Question(Base):
	__tablename__ = "question"

	id = Column("id", Integer, primary_key=True)
	poll_id = Column("poll_id", Integer, ForeignKey("poll.id"))
	question_text = Column("question_text", String, nullable=False)

	poll = relationship("Poll", back_populates="questions")
	choices = relationship("Choice", back_populates="questions")


class Choice(Base):
	__tablename__ = "choice"

	id = Column("id", Integer, primary_key=True)
	question_id = Column("question_id", Integer, ForeignKey("question.id"))
	choice_text = Column("choice_text", String, nullable=False)

	questions = relationship("Question", back_populates="choices")
	votes = relationship("Vote", back_populates="choice")


class Vote(Base):
	__tablename__ = "vote"

	id = Column("id", Integer, primary_key=True)
	choice_id = Column("choice_id", Integer, ForeignKey("choice.id"))
	user_id = Column("user_id", Integer, ForeignKey("user.id"))
	vote_timestamp = Column("vote_timestamp", TIMESTAMP)

	choice = relationship("Choice", back_populates="votes")
	user = relationship("User", back_populates="votes")
