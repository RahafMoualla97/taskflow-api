from fastapi import FastAPI
from app.routers import (
    auth,
    users,
    workspaces,
    workspace_members,
    tasks,
    task_comments,
    
)

app = FastAPI()

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(workspaces.router)
app.include_router(workspace_members.router)
app.include_router(tasks.router)
app.include_router(task_comments.router)


@app.get("/")
def root():
    return {
        "project": "TaskFlow API",
        "status": "running",
        "version": "1.0"
    }


