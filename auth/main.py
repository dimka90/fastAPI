from fastapi import Depends, FastAPI, status, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta, timezone
from pydantic import BaseModel
from typing import List, Annotated
import os
from dotenv import load_dotenv

import jwt
from pwdlib import PasswordHash
load_dotenv()
app = FastAPI()
SECRET_KEY=os.getenv("SECRET_KEY")
ALGORITHM=os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRATION_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRATION_MINUTES")
load_dotenv()
oauth2_scheme = OAuth2PasswordBearer("token")
user_next_id = 1
password_hashed = PasswordHash.recommended()


class InvalidJwtToken(HTTPException):
    def __init__(self, status_code, detail = None, headers = None):
        super().__init__(
            status_code = status_code,
            detail=detail
            )

print(password_hashed)
def generate_next_id():
    return user_next_id 

def hashed_password(password: str) -> str:
    return password_hashed.hash(password)

def verify_password(hashed_password: str, plain_password: str):
    return password_hashed.verify(hashed_password, plain_password)

result = hashed_password("james")
print(verify_password("james", result))
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

def generate_access_token( data: dict, expiry_delta: timedelta | None = None) -> str:
    encode_data = data.copy()
    if  expiry_delta:
        expire = datetime.now(timezone.utc) + expiry_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)

    encode_data.update({
        "exp": expire
    })
    encode_jwt = jwt.encode(encode_data, SECRET_KEY, algorithm=ALGORITHM)

    return encode_jwt


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> HTTPException | UserResponse:
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    user = payload.get("sub")
    if not user:
        raise InvalidJwtToken(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    active_user= find_user_by_username( user)
    if not active_user:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "User not found"
        )
    return active_user

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

    checked_user_password = verify_password(form_data.password, user.hashed_password)
    if  not checked_user_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect Password"
        )
    # ToDo
    access_token = generate_access_token( data= {
        "sub": user.username,
    }, expiry_delta=timedelta(minutes=int(ACCESS_TOKEN_EXPIRATION_MINUTES)))

    return {
        "access_token": access_token,
        "token-type": "bearer"
    }

@app.get("/api/user")
def get_user(user: Annotated[UserResponse | HTTPException, Depends(get_current_user)]):
    return user