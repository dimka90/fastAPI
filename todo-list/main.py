from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from datetime  import datetime
from typing import List, Optional
app=FastAPI()

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

@app.get("/tasks/{next_id}")
def get_task(next_id: int):
   task = find_task_by_id(next_id)
   if task is None:
      raise HTTPException(
         status_code=status.HTTP_404_NOT_FOUND,
         detail= "Invalid Id"
         )
   return  task


@app.get("/tasks")
def get_task():
   return tasks_db

@app.post("/tasks", status_code=201)
def create_task(task: TaskRequest):
   global next_id
   # to_do() -> validation 
   
   new_task = TaskResponse(
      id=next_id,
      title= task.title,
      description= task.description,
      is_completed=False,
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
