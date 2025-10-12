from fastapi import APIRouter, HTTPException, status
from ..models.user import UserInDb, UserRequest, UserResponse
from ..database.db import database_instance
from datetime import datetime
router=APIRouter()

@router.post("/users")
def create_user(id: int, user: UserRequest) -> UserResponse:

    if not user.email or not user.password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="All fields are required"
        )
    user_exit = database_instance.get_user(id)
    if  user_exit:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exist"
        )
    
    new_user = UserInDb(**user.dict(),
                        id=1,
                        created_at=datetime.utcnow(),
                        updated_at=datetime.utcnow()
    )
    is_user_create = database_instance.add_user( new_user)
    if is_user_create:
        return is_user_create
    
