from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from src.database import Base


class Choice(Base):
	__tablename__ = "choice"

	id = Column("id", Integer, primary_key=True)
	question_id = Column("question_id", Integer, ForeignKey("question.id"))
	choice_text = Column("choice_text", String, nullable=False)

	questions = relationship("Question", back_populates="choices")
	votes = relationship("Vote", back_populates="choice")
