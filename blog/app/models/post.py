from sqlmodel import SQLModel, Field
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
class Post(BaseModel):
    title: str
    content:str

class PostCreate(Post):
    image: Optional[str] = None
    author_id: int
class PostInDb(PostCreate):
    id: int = None
    created_at: datetime
    updated_at: datetime

class PostUpdate(BaseModel):
      title: Optional[str]
      content:Optional[str]
      image: Optional[str]
      author_id: Optional[str]
      updated_at: Optional[datetime]


