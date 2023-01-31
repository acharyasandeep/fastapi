from typing import List
from fastapi import status, HTTPException, Depends, APIRouter, Response
from fastapi.params import Body #for deconstructing request body
from .. import models, schemas, utils
from ..database import get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

@router.get("/", response_model = List[schemas.PostResponse])
def get_posts(db: Session = Depends(get_db)):

    # cursor.execute("""SELECT * from posts""")
    # posts = cursor.fetchall()

    posts = db.query(models.Post).all()
    return posts

@router.post("/", response_model = schemas.PostResponse)
def create_posts(new_post: schemas.CreatePost, response: Response, db: Session = Depends(get_db)):
   
    # cursor.execute(""" INSERT INTO posts(title, content, published)
    # VALUES(%s, %s, %s) RETURNING * ;""", (new_post.title, new_post.content, new_post.published))
    # created_post = cursor.fetchone()
    # conn.commit()

    
    created_post = models.Post(**new_post.dict())
    db.add(created_post)
    db.commit()
    db.refresh(created_post)

    response.status_code = status.HTTP_201_CREATED
    return created_post

@router.get("/latest", response_model = schemas.PostResponse)
def get_latest_post( db: Session = Depends(get_db)):
    
    # cursor.execute("""SELECT * FROM posts ORDER BY ID DESC LIMIT 1;""")
    # post = cursor.fetchone()

    post = db.query(models.Post).order_by(models.Post.id.desc()).first()
    return post

@router.get("/{id}", response_model = schemas.PostResponse)
def get_post(id: int, db: Session = Depends(get_db)):

    # cursor.execute("""SELECT * FROM posts WHERE id=%s;""", (id,))
    # post = cursor.fetchone()

    post = db.query(models.Post).filter(models.Post.id == id).first()


    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
        detail=f"post with id:{id} not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"post with id:{id} not found"}

    return post

@router.delete("/{id}")
def delete_post(id:int, response: Response,  db: Session = Depends(get_db)):

    # cursor.execute("""DELETE FROM posts WHERE id=%s RETURNING *;""",(id,))
    # deleted_post = cursor.fetchone()
    # conn.commit()

    deleted_post = db.query(models.Post).filter(models.Post.id == id)

    if not deleted_post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
        detail=f"post with id: {id} not found")

    deleted_post.delete(synchronize_session=False)
    db.commit()
    
    response.status_code = status.HTTP_200_OK
    return {'message': f'Post with id: {id} successfully deleted'}


@router.put("/{id}", response_model = schemas.PostResponse)
def update_post(id:int, update_post: schemas.UpdatePost, response: Response,  db: Session = Depends(get_db)):
   
    # cursor.execute("""SELECT * FROM posts WHERE id=%s ;""", (id,))
    # post = cursor.fetchone()
   
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first().__dict__

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
        detail=f"post with id:{id} not found")

    update_post_dict = update_post.dict()
    for prop in update_post_dict:
        if update_post_dict[prop] == None:
            update_post_dict[prop] = post[prop]

    # cursor.execute("""UPDATE posts SET title=%s, content=%s, published=%s WHERE id=%s RETURNING *;""",(update_post_dict['title'], update_post_dict['content'], update_post_dict['published'], id))
    # conn.commit()
    # updated_post = cursor.fetchone()

    post_query.update(update_post_dict, synchronize_session=False)
    db.commit()

    response.status_code = status.HTTP_200_OK

    return post_query.first()