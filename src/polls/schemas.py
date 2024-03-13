import datetime

from pydantic import BaseModel, constr, FutureDatetime


class CreatePoll(BaseModel):
	id: int
	title: constr(min_length=5, max_length=60)
	description: str
	end_date: FutureDatetime  # 2024-03-09 18:56:03.085849


class CreateQuestion(BaseModel):
	question_text: constr(min_length=1, max_length=40)


class CreateChoice(BaseModel):
	choice_text: constr(min_length=1, max_length=20)


class CreateVote(BaseModel):
	vote_ts: datetime.datetime


class ReadChoice(BaseModel):
	id: int
	choice_text: str


class ReadQuestion(BaseModel):
	id: int
	question_text: str
	choices: list[ReadChoice]


class ReadPoll(BaseModel):
	id: int
	title: str
	description: str
	questions: list[ReadQuestion]

