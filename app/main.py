#To run server run: uvicorn packagename.filename:instance_name --reload
#For our project : uvicorn app.main:app --reload

from fastapi import FastAPI
from fastapi.params import Body #for deconstructing request body
import psycopg2 #for postgresq
from psycopg2.extras import RealDictCursor
import time
from . import models
from .database import engine
from .routers import post, user

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

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

app.include_router(post.router)
app.include_router(user.router)

@app.get("/")
def root():
    return {"message": "Welcome to my API"}