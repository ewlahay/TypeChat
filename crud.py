from datetime import datetime
import bleach
from fastapi import HTTPException
from sqlalchemy import desc, asc
from sqlalchemy.orm import Session

import models
import schemas


def get_post(db: Session, post_id: int):
    return db.query(models.Post).filter(models.Post.id == post_id).first()


def get_sort(sort: str):
    sortBy = {
        "new": [desc(models.Post.posted)],
        "hot": (desc(models.Post.replyCount),desc(models.Post.posted)),
        "recent": [desc(models.Post.posted)],
        "oldest": [asc(models.Post.posted)]
    }
    if sortBy[sort] is None:
        raise HTTPException(400, "Invalid sort method")
    return sortBy[sort]


def get_posts(db: Session, skip: int = 0, limit: int = 100, sort="new"):
    return db.query(models.Post).order_by(*get_sort(sort)).filter(models.Post.reply == None).offset(
        skip).limit(limit).all()


def get_post_replies(db, post_id, skip: int = 0, limit: int = 100, sort="new"):
    return db.query(models.Post).order_by(*get_sort(sort)).filter(models.Post.reply == post_id).offset(
        skip).limit(limit).all()


def create_post(db: Session, post: schemas.PostBase, save=True):
    args = post.dict()
    args.pop('tp', None)
    args["subject"] = bleach.clean(post.subject)
    args["body"] = bleach.clean(post.body)
    db_item = models.Post(**args, posted=datetime.now())
    if save:
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
    return db_item


def create_post_reply(db, post, post_id):
    parent = get_post(db, post_id)
    if parent is None:
        raise HTTPException(status_code=404, detail="Post not found")
    args = post.dict()
    args.pop('tp', None)
    db_item = create_post(db, post, False)
    db_item.reply = post_id
    parent.replyCount = parent.replyCount + 1
    db.add(db_item)
    db.add(parent)
    db.commit()
    db.refresh(db_item)
    return db_item


def user_exists(db, username) -> bool:
    return db.query(models.Post).filter(models.Post.username == username).first() is not None


def get_user_posts(db, username, sort="new"):
    return db.query(models.Post).filter(models.Post.username == username).order_by(*get_sort(sort)).all()


def get_replies_to_user(db, user_id, sort):
    posts = get_user_posts(db, user_id)
    replies = []
    for post in posts:
        for reply in post.replies:
            replies.append(reply)
    sortBy = {
        "new": lambda x: x.posted,
        "hot": lambda x: (x.replyCount, x.posted),
        "recent": lambda x: x.posted,
        "oldest": lambda x: x.posted
    }
    reverse = sort != "oldest"
    replies.sort(reverse=reverse, key=sortBy[sort])
    return replies


def update_post(db, post: models.Post, updated_post):
    post.subject = bleach.clean(updated_post.subject)
    post.body = bleach.clean(updated_post.body)
    post.posted = datetime.now()
    db.add(post)
    db.commit()
    db.refresh(post)
    return post


def delete_post(db, post):
    db.delete(post)
    db.commit()


