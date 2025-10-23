from fastapi import APIRouter, status, HTTPException
from ..models.post import Post
from ..database.db import DataBase
from ..database.db import database_instance
from typing import List
postRouter = APIRouter()
@postRouter.get("/posts/{user_id}", tags=["posts"], response_model= List[Post], status_code=200)
def get_posts(user_id: int) -> List[Post] | None:
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail = "User Id can not be empty"
        )
    # Check in the db
    posts = database_instance.get_user(user_id=user_id)
    if not posts:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return database_instance._posts[user_id]

    
# create Post
@postRouter.post("/posts", tags=["past"], response_model= Post, status_code=201 )
def create_post(user_id: int,  post: Post):
    # Validation
    if not post.author_id or  not post.title:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error: Fields can not be empty"
        )
    commit = database_instance.add_post(user_id = user_id, post=post)
    if not commit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User with such  Id does not exist"
        )
    return  post
