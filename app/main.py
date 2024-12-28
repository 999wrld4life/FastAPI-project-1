from fastapi import FastAPI, Depends
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models
from .database import engine, get_db
from sqlalchemy.orm import Session
from .routers import post, user

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)

while True:
    try:
        conn = psycopg2.connect(
            host='localhost', dbname='fastapi', user='postgres', password='juicewrld999', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connected successfully")
        break
    except Exception as error:
        print("Connecting to database failed!")
        print("Error", error)
        time.sleep(2)


my_posts = [{"title": "Post one", "content": "Content of post one", "id": 1}, {
    "title": "Post two", "content": "Content of post two", "id": 2}]


def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p


def find_post_index(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i


@app.get("/")
async def root():
    return {"message": "welcome to my api!!!"}


@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"data": posts}
