from sqlmodel import SQLModel, Field
from typing import Optional
class Post(SQLModel, table = True):
    id: int
    title: str 
    content: str
    image: Optional[None] = None
    author_id: int


