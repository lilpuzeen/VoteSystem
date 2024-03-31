from pydantic import BaseModel
from fastapi import UploadFile


class CreateImage(BaseModel):
	file: UploadFile


class UpdateImage(CreateImage):
	pass
