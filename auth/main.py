from fastapi import FastAPI, status
from datetime import datetime
from pydantic import BaseModel

app = FastAPI()

class UserResquest(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    created_at: datetime
    updated_at: datetime

class UserInDB(UserResponse):
    hashed_password: str


@app.get("/api/home")
def index():
    return{
        "Message": "Hello, World"
    }

@app.post("api/users/", status_code=status.HTTP_201_CREATED)
def create_user(user: )