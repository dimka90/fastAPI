from fastapi import APIRouter
postRouter = APIRouter()

@postRouter.get("/posts", tags=["posts"])
def get_posts():
    return {
        "message": "All Posts"
    }