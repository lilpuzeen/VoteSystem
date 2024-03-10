from pydantic import BaseModel, constr, FutureDatetime


class CreatePoll(BaseModel):
	id: int
	title: constr(min_length=5, max_length=60)
	description: str
	end_date: FutureDatetime  # 2024-03-09 18:56:03.085849


class CreateQuestion(BaseModel):
	id: int
	question_text: constr(min_length=1, max_length=40)


class CreateChoice(BaseModel):
	id: int
	choice_text: constr(min_length=1, max_length=20)


