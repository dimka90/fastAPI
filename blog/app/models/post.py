from sqlmodel import SQLModel, Field
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
class Post(BaseModel):
    title: str 
    content: str
    image: Optional[str] = None
    author_id: int
    created_at: datetime
    updated_at: datetime