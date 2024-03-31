import datetime

from pydantic import BaseModel


class CreateVote(BaseModel):
	vote_ts: datetime.datetime


class UpdateVote(BaseModel):
	id: int
