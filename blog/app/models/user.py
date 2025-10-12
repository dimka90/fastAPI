from sqlmodel import SQLModel
from enum import Enum
from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class Role(str, Enum):
    ADMIN="admin"
    READER= "reader"
    AUTHOR= "author"

class User(BaseModel):
    email: str
    role: Optional[Role] = Role.AUTHOR

class UserRequest(User):
    password: str

class UserInDb(UserRequest):
    id: int
    created_at: datetime
    updated_at: datetime
class UserResponse(User):
    created_at: datetime
    updated_at: datetime
