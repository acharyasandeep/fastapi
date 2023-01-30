#To run server run: uvicorn packagename.filename:instance_name --reload
#For our project : uvicorn app.main:app --reload

from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body #for deconstructing request body
from pydantic import BaseModel #for schema validation
from random import randrange
import psycopg2 #for postgresq
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    # rating: Optional[int] = None

class UpdatePost(BaseModel):
    title: Optional[str]
    content: Optional[str]
    published: Optional[bool]
    # rating: Optional[int]

while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', 
        password='postgres', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database Connection Successful")
        break
    except Exception as error:
        print("Connection failed")
        print("Error: ", error)
        time.sleep(2)

@app.get("/")
def root():
    return {"message": "Welcome to my API"}

@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * from posts""")
    posts = cursor.fetchall()
    return {"data": posts}

@app.post("/posts")
def create_posts(new_post: Post, response: Response):
    cursor.execute(""" INSERT INTO posts(title, content, published)
    VALUES(%s, %s, %s) RETURNING * ;""", (new_post.title, new_post.content, new_post.published))
    created_post = cursor.fetchone()
    conn.commit()
    response.status_code = status.HTTP_201_CREATED
    return {"New post": created_post}

@app.get("/posts/latest")
def get_latest_post():
    cursor.execute("""SELECT * FROM posts ORDER BY ID DESC LIMIT 1;""")
    post = cursor.fetchone()
    return {"latest": post}

@app.get("/posts/{id}")
def get_post(id: int, response: Response):

    cursor.execute("""SELECT * FROM posts WHERE id=%s;""", (id,))
    post = cursor.fetchone()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
        detail=f"post with id:{id} not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"post with id:{id} not found"}

    return {"post": post}

@app.delete("/posts/{id}")
def delete_post(id:int, response: Response):

    cursor.execute("""DELETE FROM posts WHERE id=%s RETURNING *;""",(id,))
    deleted_post = cursor.fetchone()
    conn.commit()

    if not deleted_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
        detail=f"post with id: {id} not found")
    
    response.status_code = status.HTTP_200_OK
    return {'message': f'Post with id: {id} successfully deleted'}


@app.put("/posts/{id}")
def update_post(id:int, update_post:UpdatePost, response: Response):
    cursor.execute("""SELECT * FROM posts WHERE id=%s ;""", (id,))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
        detail=f"post with id:{id} not found")

    update_post_dict = update_post.dict()

    for prop in update_post_dict:
        if update_post_dict[prop] == None:
            update_post_dict[prop] = post[prop]


    cursor.execute("""UPDATE posts SET title=%s, content=%s, published=%s WHERE id=%s RETURNING *;""",(update_post_dict['title'], update_post_dict['content'], update_post_dict['published'], id))
    conn.commit()
    updated_post = cursor.fetchone()
    response.status_code = status.HTTP_200_OK

    return {"updated post: ": updated_post}


