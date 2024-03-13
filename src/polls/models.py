from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey
from src.database import Base

import datetime

# TODO: Response models
class Poll(Base):
	__tablename__ = "poll"

	id = Column("id", Integer, primary_key=True)
	title = Column("title", String, nullable=False, unique=True)
	description = Column("description", String)
	created_by = Column("created_by", Integer, ForeignKey("user.id"), nullable=False)
	start_date = Column("start_date", TIMESTAMP, default=datetime.datetime.now())
	end_date = Column("end_date", TIMESTAMP, nullable=False)


class Question(Base):
	__tablename__ = "question"

	id = Column("id", Integer, primary_key=True)
	poll_id = Column("poll_id", Integer, ForeignKey("poll.id"))
	question_text = Column("question_text", String, nullable=False)


class Choice(Base):
	__tablename__ = "choice"

	id = Column("id", Integer, primary_key=True)
	question_id = Column("question_id", Integer, ForeignKey("question.id"))
	choice_text = Column("choice_text", String, nullable=False)


class Vote(Base):
	__tablename__ = "vote"

	id = Column("id", Integer, primary_key=True)
	choice_id = Column("choice_id", Integer, ForeignKey("choice.id"))
	user_id = Column("user_id", Integer, ForeignKey("user.id"))
	vote_timestamp = Column("vote_timestamp", TIMESTAMP)
