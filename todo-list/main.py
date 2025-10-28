from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional, Dict
app = FastAPI(title="Todo list")

class User(BaseModel):
    username: str
class UserCreate(User):
    password: str
class UserInDb(UserCreate):
    created_at: datetime
    updated_at: datetime

class UserResponse(User):
    created_at: datetime
    updated_at: datetime

class TaskCreate(BaseModel):
    title: str
    description: str

class TaskinDb(TaskCreate):
    id: int
    created_at: datetime
    updated_at: datetime
    is_completed: bool 

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None

class Database:
    def __init__(self):
        self._users: Dict[int,UserInDb] = {}
        self._task:Dict[int, List[TaskinDb]]= {}
        self.id_task= 1
        self.user_id = 1
    def add_task(self, user_id:int, task:TaskinDb):
        self._task.setdefault(user_id, []).append(task)
    
    def get_tasks(self):
        return self._task
    def update_task(self, task_id: int, user_tasks: List[TaskinDb], task_to_update):
        for index, task in enumerate(user_tasks):
            if task.id == task_id:
                task_update = task.model_dump()
                task_update.update(task_to_update)
                task.updated_at = datetime.utcnow()
                task_to_store = TaskinDb(**task_update)
                user_tasks[index] = task_to_store
                break
        return user_tasks
    def increment_id_task(self):
        self.id_task+= 1
    def increment_id_user(self): 
        self.user_id += 1

    def add_user(self, user: UserInDb) -> UserInDb | None:
        for _, user_details in self._users.items():
            if user_details.username == user.username:
                return None
        user_id= self.user_id
        self._users[user_id] = user
        self.increment_id_user()
        return user
    
    def get_all_users(self):
        return self._users
    
    def check_user_exist(self, user_id:int):
        if not user_id in self._users:
            return None
        return user_id
    def get_all_user_tasks(self, user_id: int) -> List[TaskinDb]:
        user_tasks = None
        for id_in_db, user_task in self._task.items():
            if id_in_db == user_id:
                user_tasks = user_task
                break
        return user_tasks
    
class USERNOTFOUNDERROR(HTTPException):
    def __init__(self, status_code=status.HTTP_404_NOT_FOUND, detail = "User not found", headers = None):
        super().__init__(status_code, detail, headers)
        pass
        
db_instance = Database()

# Endpoints

@app.get("/")
def index():
    return{
        "message": "Todo App"
    }

@app.post("/tasks", status_code=status.HTTP_201_CREATED)
def create_task(task: TaskCreate, user_id: int):
    if not task.title or not task.description:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="All fields are required"
        )
    user_id = db_instance.check_user_exist(user_id)
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User does not exist"
        )
    

    new_task = TaskinDb(
        title=task.title,
        description= task.description,
        id =db_instance.id_task,
        created_at= datetime.utcnow(),
        updated_at=datetime.utcnow(),
        is_completed=False
    )
    db_instance.increment_id_task()
    db_instance.add_task(user_id=user_id, task=new_task)

    return {
        "success": True,
        "data": new_task,
        "message": "Task created successfully"
    }


@app.get("/tasks")
def get_user_tasks(id:int ):
    user_id = db_instance.check_user_exist(id)
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User does not exist"
        )
    user_tasks = db_instance.get_all_user_tasks(user_id)
    return {
        "data": user_tasks,
         "message": "All User tasks retrived successfully"
    }

@app.get("/tasks/")
def get_all_task():
   tasks =  db_instance.get_tasks()
   return{
       "success": True,
       "data": tasks,
       "message": "All tasks retrived successfully"
   }



@app.patch("/tasks/")
def update(task: TaskUpdate, user_id: int, task_id: int):
    """
    Update:
            Partial task update
    Arg:
        task: A pydantic model of Task (title or description)
    Return Type:
                 HTTPException | Task
    """
    if not task.title and not task.description:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="Atleast One field is required"
        )
    # Check if user exist
    user_id= db_instance.check_user_exist(user_id)
    if not user_id:
        raise USERNOTFOUNDERROR()
    user_tasks = db_instance.get_all_user_tasks(user_id)
    filter_task = task.model_dump(exclude_unset=True)
    tasks = db_instance.update_task(task_id,user_tasks,filter_task)
    return tasks
    # todo , check if user has any asks
#============================
# User endpoints

@app.post("/users")
def register_user(user: UserCreate):
    if not  user.username or  not user.password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="All Fields are required"
        )
    new_user = UserInDb(
        **user.model_dump(),
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()                   
    )
    user = db_instance.add_user(new_user)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already exist"
            )
    return {
        "success": True,
        "data": UserResponse(**user.model_dump(exclude_unset=True)),
        "message": "User created Successfully"
    }
   
@app.get("/users")
def get_users():
    users = db_instance.get_all_users()
    return {
        "success": True,
        "data": users,
        "message": "All Users retrived  Successfully"
    }