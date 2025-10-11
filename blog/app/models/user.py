from sqlmodel import SQLModel
from enum import Enum
class Role(str, Enum):
    Admin=str
    Reader= str
    Author=str

class User(SQLModel):
    id: int
    email: str
    Role: Role
    password: str
    