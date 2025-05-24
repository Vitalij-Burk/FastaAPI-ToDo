import uuid
from typing import Optional

from models.schemas.base import TunedModel
from pydantic import BaseModel


class ShowTask(TunedModel):
    task_id: uuid.UUID
    task: str
    status: str
    # authors: list[uuid.UUID]
    # producers: list[uuid.UUID]


class CreateTask(BaseModel):
    producers_ids: list[uuid.UUID]
    task: str


class UpdateTaskRequest(BaseModel):
    task: Optional[str] = None


class UpdatedTaskResponse(BaseModel):
    updated_task_id: uuid.UUID


class DeletedTaskResponse(BaseModel):
    deleted_task_id: uuid.UUID


class RestoredTaskResponse(BaseModel):
    restored_task_id: uuid.UUID
