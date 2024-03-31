from pydantic import BaseModel, constr

from src.polls.choice.schemas import ReadChoice


class CreateQuestion(BaseModel):
	question_text: constr(min_length=1, max_length=40)


class ReadQuestion(BaseModel):
	id: int
	question_text: str
	choices: list[ReadChoice]


class UpdateQuestion(CreateQuestion):
	pass
