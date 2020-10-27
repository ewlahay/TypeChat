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


class UserResponse:
	message: str
	message_code: int
	success: int
	count: int
	mobilecount: int
	type: str
	status: int

	def __init__(self, message, message_code, success, count, mobilecount, type, status):
		self.message = message
		self.message_code = message_code
		self.success = success
		self.count = count
		self.mobilecount = mobilecount
		self.type = type
		self.status = status


class TypingPattern:
	deviceType: int
	deviceModel: int
	deviceId: int
	isMobile: int
	operatingSystem: int
	programmingLanguage: int
	systemLanguage: int
	isTouchDevice: int
	pressType: int
	keyboardInput: int
	keyboardType: int
	pointerInput: int
	browserType: int
	displayWidth: int
	displayHeight: int
	orientation: int
	osVersion: int
	browserVersion: int
	cookieId: int
	signature: int

	def __init__(self, pattern: str):
		args = pattern.split(",")
		args = args[len(args) - 20:len(args)]
		self.deviceType = int(args[0])
		self.deviceModel = int(args[1])
		self.deviceId = int(args[2])
		self.isMobile = int(args[3])