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

def find_user_by_username( username: str) -> UserResponse  | None:
    for user in user_db:
        if user.username == username:
            return user
    return None

def check_password_match(user: UserInDB, password) ->bool:
    pwd_in_db = user.hashed_password
    if  pwd_in_db == password:
        return True
    return False
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
    user_name = form_data.username
    user = find_user_by_username( user_name)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="user does not exist"
        )
    user_password = form_data.password
    checked_user_password = check_password_match(user, user_password)
    if  not checked_user_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect Password"
        )
    # ToDo
    return {
        "access-token": user.username,
        "token-type": "bearer"
    }
