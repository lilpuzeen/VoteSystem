from pydantic import BaseModel, constr, FutureDatetime
from src.polls.question.schemas import ReadQuestion


class CreatePoll(BaseModel):
	id: int
	title: constr(min_length=5, max_length=60)
	description: str
	end_date: FutureDatetime  # 2024-03-09 18:56:03.085849


class ReadPoll(BaseModel):
	id: int
	title: str
	description: str
	questions: list[ReadQuestion]


class UpdatePoll(BaseModel):
	title: constr(min_length=5, max_length=60)
	description: str
	end_date: FutureDatetime  # 2024-03-09 18:56:03.085849
