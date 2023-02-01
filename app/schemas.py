from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime

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

class PostResponse(BaseModel):
    id: int
    title: str
    content: str
    published: bool
    created_at: datetime
    class Config:
        orm_mode = True

class CreateUser(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: str
    email: EmailStr
    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class TokenData(BaseModel):
    id: Optional[str] = None

class Token(BaseModel):
    token: str
    token_type: str