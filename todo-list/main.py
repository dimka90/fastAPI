from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from datetime  import datetime
from typing import List, Optional
app=FastAPI()

task_id = 1

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


tasks_db : List[TaskResponse]= []
# POST   /tasks              - Create new task
# GET    /tasks              - Get all tasks
# GET    /tasks/{task_id}    - Get specific task
# PUT    /tasks/{task_id}    - Update task
# DELETE /tasks/{task_id}    - Delete task
# PATCH  /tasks/{task_id}/complete - Toggle completion


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


@app.get("/tasks/{task_id}")
def get_task(task_id: int):
   task = find_task_by_id(task_id)
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
   global task_id
   # to_do() -> validation 
   
   new_task = TaskResponse(
      id=task_id,
      title= task.title,
      description= task.description,
      is_completed=False,
      created_at= datetime.utcnow(),
      updated_at=datetime.utcnow()
   )
   task_id += 1
   tasks_db.append(new_task)

   return  new_task


@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int):
   task = find_task_by_id(task_id)
   if task is None:
      raise HTTPException(
         status_code=status.HTTP_404_NOT_FOUND,
         detail="Invalid Id"
      )
   tasks_db.remove(task)
   return None
   
# @app.put("/tasks/{task_id}")
# def update_a_task(task_id:int , task: Task):
#    print(task_id)
#    if task_id > len(tasks_db):
#       return {
#         "success": False,
#          "message" : "Invalid task Id"
#       }
#    tasks_db[task_id - 1] = task
#    tasks_db[task_id-1].id = task_id
#    return {
#       "success": True,
#       "data": tasks_db[task_id -1],
#       "message": "All field updated successfully"
#    }

 