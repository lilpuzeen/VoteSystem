from typing import Optional

from pydantic import BaseModel
# TODO: correct schemas for each entity


class HTTPError(BaseModel):
    detail: str


class PostBase(BaseModel):
    title: Optional[str] = None
    body: Optional[str] = None


class PostCreate(PostBase):
    title: str
    body: str


class PostUpdate(PostBase):
    pass
