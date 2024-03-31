from pydantic import BaseModel, constr


class CreateChoice(BaseModel):
	choice_text: constr(min_length=1, max_length=20)


class ReadChoice(BaseModel):
	id: int
	choice_text: str


class UpdateChoice(CreateChoice):
	pass
