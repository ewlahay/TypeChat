import base64
import hashlib
import random
from typing import List

import requests
import uvicorn
from fastapi import FastAPI, Depends, Request, HTTPException, Path
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from starlette.templating import Jinja2Templates

import crud
import models
import schemas
from database import SessionLocal, engine
from settings import Settings

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

base_url = 'https://api.typingdna.com'
settings = Settings()
authString = '%s:%s' % (settings.api_key, settings.api_secret)
base64string = base64.encodestring(authString.encode()).decode().replace('\n', '')
templates = Jinja2Templates(directory="app/dist")
origins = [
    "http://localhost:3000",
    "127.0.0.1:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

'''
@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    response = Response("Internal server error", status_code=500)
    try:
        request.state.db = SessionLocal()
        response = await call_next(request)
    finally:
        request.state.db.close()
    return response


# Dependency
def get_db(request: Request):
    return request.state.db
'''


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/hello")
async def root():
    return {"message": "Hello World\n Check out /docs for details"}


@app.post("/api/posts", response_model=schemas.Post, tags=["posts"])
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
    """
    Create an post with all the information:

    - **username**: the username to post as
    - **subject**: the title of the post
    - **body**: The main body of the post. Supports markdown
    - **tp**: A captured typing pattern to authenticate the user
    """
    if not user_exists(db, post.username):
        if save_user(post.username, post.tp):
            return crud.create_post(db, post)
        else:
            raise HTTPException(status_code=400, detail="Unable to save user")
    elif verify_user(post.username, post.tp):
        return crud.create_post(db, post)
    raise HTTPException(status_code=401, detail="Unable to authenticate user")


@app.get("/api/posts", response_model=List[schemas.Post], tags=["posts"])
def get_posts(skip: int = 0, limit: int = 100, sort: str = "new", db: Session = Depends(get_db)):
    """
        Get all posts

        - **skip**: the offset of where to start getting posts ie skip = 10 would start with the 11th post
        - **limit**: maximum number of posts to get
        - **sort**: How query should be sorted, can be new, hot, recent, oldest
    """
    return crud.get_posts(db, skip=skip, limit=limit, sort=sort)


@app.get("/api/posts/{post_id}", response_model=schemas.Post, tags=["posts"])
def get_post(post_id: int, db: Session = Depends(get_db)):
    post = crud.get_post(db=db, post_id=post_id)
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


@app.put("/api/posts/{post_id}", response_model=schemas.Post, tags=["posts"])
def update_post(post_id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db)):
    post = crud.get_post(db=db, post_id=post_id)
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    if verify_user(updated_post.username, updated_post.tp):
        return crud.update_post(db, post, updated_post)
    raise HTTPException(status_code=401, detail="Unable to authenticate user")


@app.delete("/api/posts/{post_id}", tags=["posts"])
def delete_post(post_id: int, delete_post: schemas.Base, db: Session = Depends(get_db)):
    post = crud.get_post(db=db, post_id=post_id)
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    if verify_user(post.username, delete_post.tp):
        crud.delete_post(db, post)
        return HTTPException(status_code=204)
    raise HTTPException(status_code=401, detail="Unable to authenticate user")


@app.get("/api/posts/{post_id}/replies", response_model=List[schemas.Post], tags=["posts", "replies"])
def get_post_replies(post_id: int, skip: int = 0, limit: int = 100, sort: str = "new", db: Session = Depends(get_db)):
    return crud.get_post_replies(db, post_id, skip, limit, sort)


@app.get("/api/users/{user_id}", response_model=List[schemas.Post], tags=["users"])
def get_user_posts(user_id: str, sort: str = "new", db: Session = Depends(get_db)):
    return crud.get_user_posts(db, user_id, sort)


@app.get("/api/users/{user_id}/replies", response_model=List[schemas.Post], tags=["users", "replies"])
def get_replies_to_user(user_id: str, sort: str = "new", db: Session = Depends(get_db)):
    return crud.get_replies_to_user(db, user_id, sort)


@app.post("/api/posts/{post_id}/reply", response_model=schemas.Post, tags=["posts", "replies"])
def create_reply(post: schemas.PostCreate, post_id: int, db: Session = Depends(get_db)):
    if not user_exists(db, post.username):
        if save_user(post.username, post.tp):
            return crud.create_post_reply(db, post, post_id)
        else:
            raise HTTPException(status_code=400, detail="Unable to save user")
    elif verify_user(post.username, post.tp):
        return crud.create_post_reply(db, post, post_id)
    raise HTTPException(status_code=401, detail="Unable to authenticate user")


@app.post("/api/users/{user_id}", tags=["users"])
def save_pattern(post: schemas.Base, user_id: str, db: Session = Depends(get_db)):
    if user_exists(db, user_id):
        if verify_user(username=user_id, typingPattern=post.tp):
            if save_user(user_id, post.tp):
                return "pattern saved"
            else:
                raise HTTPException(status_code=400, detail="Unable to save user")
        else:
            raise HTTPException(status_code=401, detail="Unable to authenticate user")
    else:
        raise HTTPException(status_code=404, detail="User not found")


@app.get("/api/text")
def get_text():
    return random_text(texts)


@app.get("/api/markdown")
def get_random_markdown():
    return random_text(markdown)


@app.get("/api/markdown/{markdown_id}")
def get_markdown(markdown_id: int):
    try:
        return markdown[markdown_id]
    except IndexError:
        raise HTTPException(status_code=404, detail="Markdown example not found")


@app.route("/{post:int}")
async def catch_all(request: Request, post: int = Path(..., ge=0)):
    print("Getting catchall")
    print("full_path: ", post)
    return templates.TemplateResponse("index.html", {"request": request})


@app.route("/users/{user:path}")
async def catch_all(request: Request, user: str = Path(...)):
    print("Getting ", user)
    return templates.TemplateResponse("index.html", {"request": request})


app.mount("/", StaticFiles(directory="app/dist", html=True), name="static")


def user_exists(db, username: str) -> bool:
    if crud.user_exists(db, username):
        return True

    id = get_user_id(username)
    url = '%s/user/%s' % (base_url, id)

    res = requests.get(url, headers={"Authorization": "Basic %s" % base64string})
    print("\n\nchecking for user:")
    print(res.text)
    print()
    data = res.json()
    if data["count"] > 0 or data["mobilecount"] > 0:
        return True
    print("User doesn't exist")
    return False


def save_user(username: str, typingPattern: str) -> bool:
    userId = get_user_id(username)
    url = '%s/save/%s' % (base_url, userId)
    print(url, typingPattern, userId)
    res = requests.post(url, data={'tp': typingPattern}, headers={"Authorization": "Basic %s" % base64string,
                                                                  "Content-type": "application/x-www-form-urlencoded"})

    print("\n\nsaving user: (duplicates are ok here)")
    print(res.text)
    return res.status_code == requests.codes.ok


def verify_user(username: str, typingPattern: str):
    #sleep(2.5)
    #return True

    id = get_user_id(username)
    url = '%s/verify/%s' % (base_url, id)
    res = requests.post(url, data={'tp': typingPattern, 'quality': "1"},
                        headers={"Authorization": "Basic %s" % base64string,
                                 "Content-type": "application/x-www-form-urlencoded"})
    print("\n\nVerifying user:")
    print(res.text)
    data = res.json()
    if res.status_code == requests.codes.ok:
        try:
            if data["success"] == 1 and data["result"] == 1:
                print(username, " is valid")
                return True
        except KeyError:
            if data["message_code"] == 10:  # Pattern automatically enrolled
                return True
    raise HTTPException(status_code=401, detail=data["message"])


def get_user_id(username: str) -> str:
    return hashlib.md5(username.encode() + settings.secret_key.encode()).hexdigest()


texts = [
    "I solemly swear I am up to no good"
]

markdown = [
    "# This is the title of a post",
    "Check out this https://example.com",
    "Create ~strike through text~",
    "You can create relative links using [link](1)",
    "__This is how you can make bold text__",
    "**This is a way to make text bold**",
    "* bullet\n* points\n* make\n* everything\n* better",
    "Numbered list:\n1. first\n2. second\n3. third",
    "Create a line with\n***",
    "* Create a list by starting with +, -, or *\n  * Indent 2 spaces for a sub-list",
    "Create a table with\n\n| Number | Phrase |\n| -- | -- |\n| 1 | my clown car |",
    "Insert a picture with\n\n![](https://placekitten.com/200 \"I can has cheezburger?\")",
]


def random_text(array) -> str:
    return array[random.randint(0, len(array) - 1)]


if __name__ == "__main__":
    uvicorn.run(app=app, port=8000)