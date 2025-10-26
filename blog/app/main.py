from fastapi import FastAPI, Depends
from .routers.posts import postRouter
from .routers import users
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")
app = FastAPI(title="Blog")
app.include_router(postRouter)
app.include_router(users.router)
@app.get("/api")
def home( token: str = Depends(oauth2_scheme)):

    return {
        "token": token,
        "Message": "Welcome Home"
    }

@app.post("/token")
def login():
    return { "access_token": "1234", "token_type": "bearer"}