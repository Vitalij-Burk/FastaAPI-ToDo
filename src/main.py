import uvicorn
from api.routes.login import login_router
from api.routes.task import task_router
from api.routes.user import user_router
from fastapi import FastAPI


app = FastAPI()


app.include_router(login_router, prefix="/login", tags=["Login"])
app.include_router(user_router, prefix="/user", tags=["User"])
app.include_router(task_router, prefix="/task", tags=["Task"])


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
