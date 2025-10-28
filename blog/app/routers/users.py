from fastapi import APIRouter, HTTPException, status
from ..models.user import UserInDb, UserRequest, UserResponse
from ..database.db import database_instance
from datetime import datetime
from app.auth import verify_password, generate_hash
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
            status_code=status.HTTP_409_CONFLICT,
            detail="User already exist"
        )
    hashed_password = generate_hash(user.password)
    new_user = UserInDb(**user.dict(),
                        hashed_password=hashed_password,
                        id=id,
                        created_at=datetime.utcnow(),
                        updated_at=datetime.utcnow()
    )
    is_user_create = database_instance.add_user( new_user)
    if is_user_create:
        return is_user_create
    
# sudo lsof -i -P -n | grep LISTEN
#sudo ufw allow 8000

