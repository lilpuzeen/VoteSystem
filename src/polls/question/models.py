from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from src.database import Base


class Question(Base):
	__tablename__ = "question"

	id = Column("id", Integer, primary_key=True)
	poll_id = Column("poll_id", Integer, ForeignKey("poll.id"))
	question_text = Column("question_text", String, nullable=False)

	poll = relationship("Poll", back_populates="questions")
	choices = relationship("Choice", back_populates="questions")
