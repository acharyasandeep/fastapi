from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime

from pydantic.types import conint

class CreatePost(BaseModel):
    title: str
    content: str
    published: bool = True
    # rating: Optional[int] = None

class UpdatePost(BaseModel):
    title: Optional[str]
    content: Optional[str]
    published: Optional[bool]
    # rating: Optional[int]

class UserResponse(BaseModel):
    id: str
    email: EmailStr
    class Config:
        orm_mode = True

class PostBase(BaseModel):
    id: int
    title: str
    content: str
    published: bool
    created_at: datetime
    owner: UserResponse
    class Config:
        orm_mode = True

class PostResponse(BaseModel):
    Post: PostBase
    votes: int
    class Config:
        orm_mode = True

class CreateUser(BaseModel):
    email: EmailStr
    password: str



class UserLogin(BaseModel):
    email: EmailStr
    password: str

class TokenData(BaseModel):
    id: Optional[str] = None

class Token(BaseModel):
    token: str
    token_type: str

class Vote(BaseModel):
    post_id: int
    dir: conint(ge=0, le=1)