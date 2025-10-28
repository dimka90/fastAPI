from fastapi import APIRouter, status, HTTPException
from ..models.post import PostCreate, PostUpdate, PostInDb
from ..database.db import DataBase
from ..database.db import database_instance
from typing import List
from datetime import datetime
postRouter = APIRouter()
@postRouter.get("/posts/{user_id}", tags=["posts"], response_model= List[PostInDb], status_code=200)
def get_posts(user_id: int) -> List[PostInDb] | None:
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
@postRouter.post("/posts", tags=["past"], response_model= PostInDb, status_code=201 )
def create_post(user_id: int,  post: PostCreate):
    # Validation
    if not post.author_id or  not post.title:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error: Fields can not be empty"
        )
    post_in_db = PostInDb(
        **post.model_dump(),
        created_at=datetime.utcnow(),
        updated_at = datetime.utcnow(),
        id=database_instance.post_id()
    )
    commit = database_instance.add_post(user_id = user_id, post=post_in_db)
    if not commit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User with such  Id does not exist"
        )
    return  post_in_db

@postRouter.patch("/posts/")
def update_post(post: PostUpdate, author_id: int):
    if not post.id or not author_id:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="Post id and Authors Id are required"
        )
    # find user
    user_post = database_instance.get_user(author_id)
    if not user_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User does not Exist"
        )
    user_posts= database_instance.get_posts(author_id)
    # Call the function to get the post
    post_to_update = database_instance.update_post(user_posts, post.id, post.model_dump(exclude_unset=True))
    if  not post_to_update:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post with such Id does not exist"
        )
    
    return post_to_update
    # get user id
