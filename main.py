from fastapi import FastAPI
from fastapi.params import Body

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Welcome to my API"}

@app.get("/posts")
def get_posts():
    return {"data":"This is my posts"}

@app.post("/posts")
def create_posts(payload: dict = Body(...)):
    print(payload)
    return {"message":"Successfully created posts"}