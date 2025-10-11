from fastapi import FastAPI
from .routers.posts import postRouter
app = FastAPI(title="Blog")
app.include_router(postRouter)
@app.get("/")
def home():
    return {
        "Message": "Welcome Home"
    }