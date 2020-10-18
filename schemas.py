from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class PostBase(BaseModel):
	username: str
	subject: str
	body: str


class PostCreate(PostBase):
	tp: str


class Base(BaseModel):
	tp: str


class Post(PostBase):
	id: int
	posted: datetime
	reply: Optional[int]

	class Config:
		orm_mode = True
