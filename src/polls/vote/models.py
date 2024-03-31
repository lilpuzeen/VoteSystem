from sqlalchemy import Column, Integer, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship

from src.database import Base


class Vote(Base):
	__tablename__ = "vote"

	id = Column("id", Integer, primary_key=True)
	choice_id = Column("choice_id", Integer, ForeignKey("choice.id"))
	user_id = Column("user_id", Integer, ForeignKey("user.id"))
	vote_timestamp = Column("vote_timestamp", TIMESTAMP)

	choice = relationship("Choice", back_populates="votes")
	user = relationship("User", back_populates="votes")
