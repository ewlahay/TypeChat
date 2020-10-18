from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship, backref

from database import Base


class Post(Base):
	__tablename__ = "posts"
	id = Column(Integer, primary_key=True, index=True)
	username = Column(String, index=True)
	subject = Column(String)
	body = Column(String)
	posted = Column(DateTime)
	replyCount = Column(Integer, default=0)
	reply = Column(Integer, ForeignKey('posts.id'), nullable=True)
	parent = relationship("Post", backref="replies", remote_side=[id])
