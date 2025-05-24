import uuid
from typing import Optional

from models.schemas.base import TunedModel
from pydantic import BaseModel
from pydantic import EmailStr


class ShowUser(TunedModel):
    user_id: uuid.UUID
    username: str
    email: EmailStr
    is_active: bool
    # created_tasks: list[uuid.UUID]
    # assigned_tasks: list[uuid.UUID]


class CreateUser(BaseModel):
    username: str
    email: EmailStr
    password: str


class UpdateUserRequest(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None


class UpdatedUserResponse(BaseModel):
    updated_user_id: uuid.UUID


class DeletedUserResponse(BaseModel):
    deleted_user_id: uuid.UUID
