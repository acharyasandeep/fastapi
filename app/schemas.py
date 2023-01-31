from typing import Optional
from pydantic import BaseModel
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
