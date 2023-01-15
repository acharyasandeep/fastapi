#1:05:08 timestamp in the tutorial

#To run server run: uvicorn packagename.filename:instance_name --reload
#For our project : uvicorn app.main:app --reload

from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body #for deconstructing request body
from pydantic import BaseModel #for schema validation
from random import randrange

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

class UpdatePost(BaseModel):
    title: Optional[str]
    content: Optional[str]
    published: Optional[bool]
    rating: Optional[int]

my_posts = [
    {
        "id": 1,  
        "title":"title of post 1", 
        "content":"Content of post 1"
    },
    {
        "id": 2,
        "title":"What am I going to do with my life?",
        "content":"Learn python, learn golang and learn ML, AI"
    }
]

def find_post(id):
    for post in my_posts:
        if id == post['id']:
            return post
    
    return None

def find_index_post(id):
    for index, post in enumerate(my_posts):
        if id == post['id']:
            return index
    
    return -1


@app.get("/")
def root():
    return {"message": "Welcome to my API"}

@app.get("/posts")
def get_posts():
    return {"data": my_posts}

@app.post("/posts")
def create_posts(new_post: Post, response: Response):
    post_dict = new_post.dict()
    post_dict['id'] = randrange(0,10000000)
    my_posts.append(post_dict)
    response.status_code = status.HTTP_201_CREATED
    return {"New post": post_dict}

@app.get("/posts/latest")
def get_latest_post():
    return {"latest": my_posts[-1]}

@app.get("/posts/{id}")
def get_post(id: int, response: Response):

    post = find_post(id)

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
        detail=f"post with id:{id} not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"post with id:{id} not found"}

    return {"new post": post}

@app.delete("/posts/{id}")
def delete_post(id:int, response: Response):
    index = find_index_post(id)
    if index == -1:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
        detail=f"post with id: {id} not found")
    
    my_posts.pop(index)
    response.status_code = status.HTTP_200_OK
    return {'message': f'Post with id: {id} successfully deleted'}


@app.put("/posts/{id}")
def update_post(id:int, update_post:UpdatePost, response: Response):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
        detail=f"post with id:{id} not found")

    update_post_dict = update_post.dict()

    for prop in update_post_dict:
        if update_post_dict[prop] != None:
            post[prop] = update_post_dict[prop]

    response.status_code = status.HTTP_200_OK

    return {"posts: ": my_posts}


