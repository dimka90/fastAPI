from fastapi import FastAPI
from .routers.posts import postRouter
from .routers import users
app = FastAPI(title="Blog")
app.include_router(postRouter)
app.include_router(users.router)
@app.get("/")
def home():
    return {
        "Message": "Welcome Home"
    }