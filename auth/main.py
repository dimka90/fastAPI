from fastapi import Depends, FastAPI, status, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime
from pydantic import BaseModel
from typing import List, Annotated
app = FastAPI()


oauth2_scheme = OAuth2PasswordBearer("token")
user_next_id = 1

def generate_next_id():
    return user_next_id 

def hashed_password(password: str) -> str:
    return f"{password}+abc*"

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

user_db: List[UserInDB] = []

@app.get("/api/home")
def index():
    return{
        "Message": "Hello, World"
    }

@app.post("/api/users/", status_code=status.HTTP_201_CREATED)
def create_user(user: UserResquest) -> UserResponse:
    global user_next_id
    if not user.username :
        raise  HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User name is required"
        )
        
    if not user.password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="password field can't be empty"
        )
    password = user.password
    password = hashed_password(password)
    new_user = UserInDB(
        id=generate_next_id(),
        hashed_password=password,
        username=user.username,
        created_at= datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    user_next_id += 1
    user_response = UserResponse(**new_user.model_dump())
    # store user in Db
    user_db.append(new_user)
    
    return user_response

@app.post("/token")
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    