#To run server run: uvicorn packagename.filename:instance_name --reload
#For our project : uvicorn app.main:app --reload

from fastapi import FastAPI
from . import models
from .database import engine
from .routers import post, user, auth, vote


# models.Base.metadata.create_all(bind=engine) #we can use alembeic, no longer needed to create tables at restart
app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
def root():
    return {"message": "Welcome to my API"}