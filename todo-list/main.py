from fastapi import FastAPI, HTTPException, status, Depends
from pydantic import BaseModel, Field
from datetime  import datetime
from fastapi.security import OAuth2PasswordBearer
from typing import List, Optional, Annotated
app=FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
next_id = 1

class TaskRequest(BaseModel):
   title: str
   description: str | None

class TaskResponse(BaseModel):
   id: int
   title: str
   description: str | None
   is_completed:  bool = False
   created_at: datetime
   updated_at: datetime

class  TaskUpdate(BaseModel):
   title: Optional[str] = None
   description: Optional[str] =None

tasks_db : List[TaskResponse]= []
# POST   /tasks              - Create new task
# GET    /tasks              - Get all tasks
# GET    /tasks/{next_id}    - Get specific task
# PUT    /tasks/{next_id}    - Update task
# DELETE /tasks/{next_id}    - Delete task
# PATCH  /tasks/{next_id}/complete - Toggle completion


def find_task_by_id(id: int) -> TaskResponse| None:
   if len(tasks_db) < 0:
      return None
   for task in tasks_db:
      if task.id == id:
         return task
   return None

def find_task_by_title(title: str ) -> TaskResponse| None:
   for task in tasks_db:
      if task.title == title:
         return task
   return None

def get_current_time() -> datetime:
   return datetime.utcnow()


@app.get("/tasks")
def get_all_task():
   return tasks_db

@app.get("/tasks/{next_id}")
def get_task(next_id: int):
   task = find_task_by_id(next_id)
   if task is None:
      raise HTTPException(
         status_code=status.HTTP_404_NOT_FOUND,
         detail= "Invalid Id"
         )
   return  task


@app.post("/tasks", status_code=201)
def create_task(task: TaskRequest):
   global next_id
   # to_do() -> validation 
   
   new_task = TaskResponse(
      id=next_id,
      title= task.title,
      description= task.description,
      is_completed=True,
      created_at= datetime.utcnow(),
      updated_at=datetime.utcnow()
   )
   next_id += 1
   tasks_db.append(new_task)

   return  new_task

@app.delete("/tasks/{next_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(next_id: int):
   task = find_task_by_id(next_id)
   if task is None:
      raise HTTPException(
         status_code=status.HTTP_404_NOT_FOUND,
         detail="Invalid Id"
      )
   tasks_db.remove(task)
   return None
   
@app.put("/tasks/{next_id}", status_code=status.HTTP_206_PARTIAL_CONTENT)
def update_a_task(next_id: int, new_task: TaskUpdate) -> TaskResponse:
   task = find_task_by_id(next_id)
   if task is None:
      raise HTTPException(
         status_code=status.HTTP_404_NOT_FOUND,
         detail=" Invalid Id"
      )
   task.title = new_task.title
   task.description = new_task.description
   task.updated_at = get_current_time()
   return task

@app.patch("/tasks/{next_id}", status_code=status.HTTP_206_PARTIAL_CONTENT)
def update_a_task(next_id: int, new_task: TaskUpdate) -> TaskResponse:
   
   task_to_update = find_task_by_id(next_id)
   if task_to_update is None:
      raise HTTPException(
         status_code=status.HTTP_404_NOT_FOUND,
         detail=" Invalid Id"
      )
   if new_task.title is not None:
      task_to_update.title = new_task.title
   if new_task.description is not None:
      task_to_update.description = new_task.description

   return task_to_update

# filtering

# @app.get("/tasks", response_model= List[TaskResponse])
# def get_filter_tasks(completed: Optional[bool] = None):
#    if completed is None:
#       raise HTTPException(
#          status_code=status.HTTP_400_BAD_REQUEST,
#          detail="All fields are required"
#       )
#    completed_tasks = [ task for task in tasks_db if task.is_completed == completed]
#    if completed_tasks:
#       return completed_tasks
#    else:
#       return  []
   
@app.get("/tasks", response_model=List[TaskResponse])
def get_tasks(completed: Optional[bool] = None):
    print(f"🔍 DEBUG: completed parameter = {completed}")
    print(f"🔍 DEBUG: Total tasks in db = {len(tasks_db)}")
    
    if completed is None:
        print("🔍 DEBUG: Returning ALL tasks")
        return tasks_db
    
    filtered = [task for task in tasks_db if task.is_completed == completed]
    print(f"🔍 DEBUG: Filtered tasks count = {len(filtered)}")
    print(f"🔍 DEBUG: Looking for is_completed = {completed}")
    
    for task in tasks_db:
        print(f"  - Task {task.id}: is_completed = {task.is_completed}")
    
    return filtered

@app.get("/tasks_auth")
def authenticated_route(token: Annotated[str, Depends(oauth2_scheme)]):
   return token