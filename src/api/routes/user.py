import uuid
from logging import getLogger

from api.errors.exceptions.Forbidden import ForbiddenError
from api.errors.functions.Database import DatabaseError
from api.errors.functions.NotFound import NotFoundErrorCheck
from api.errors.functions.Unprocessable import UnprocessableError
from core.dependencies.get_db import get_db
from db.models import User
from fastapi import APIRouter
from fastapi import Depends
from models.schemas.user import CreateUser
from models.schemas.user import DeletedUserResponse
from models.schemas.user import ShowUser
from models.schemas.user import UpdatedUserResponse
from models.schemas.user import UpdateUserRequest
from services.auth import get_current_user_from_token
from services.user import _create_user
from services.user import _delete_user
from services.user import _get_user_by_id
from services.user import _update_user
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession


user_router = APIRouter()


logger = getLogger(__name__)


@user_router.post("/", response_model=ShowUser)
async def create_user(body: CreateUser, db: AsyncSession = Depends(get_db)) -> ShowUser:
    try:
        return await _create_user(body=body, session=db)
    except IntegrityError as err:
        logger.error(err)
        await DatabaseError(err)


@user_router.get("/", response_model=ShowUser)
async def get_user_by_id(
    user_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token),
) -> ShowUser:
    user = await _get_user_by_id(user_id=user_id, session=db)
    await NotFoundErrorCheck(user, "User", user_id)
    return user


@user_router.patch("/", response_model=UpdatedUserResponse)
async def update_user(
    user_id: uuid.UUID,
    body: UpdateUserRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token),
) -> UpdatedUserResponse:
    update_user_params = body.model_dump(exclude_none=True)
    if update_user_params == {}:
        await UnprocessableError("At least one parameter must be provided.")
    if user_id != current_user.user_id:
        raise ForbiddenError
    user = await _get_user_by_id(user_id=user_id, session=db)
    await NotFoundErrorCheck(user, "User", user_id)
    updated_user_id = await _update_user(
        user_id=user_id, update_user_params=update_user_params, session=db
    )
    await NotFoundErrorCheck(updated_user_id, "User", user_id)
    return UpdatedUserResponse(updated_user_id=updated_user_id)


@user_router.delete("/", response_model=DeletedUserResponse)
async def delete_user(
    user_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token),
) -> DeletedUserResponse:
    if user_id != current_user.user_id:
        raise ForbiddenError
    deleted_user_id = await _delete_user(user_id=user_id, session=db)
    await NotFoundErrorCheck(deleted_user_id, "User", user_id)
    return DeletedUserResponse(deleted_user_id=deleted_user_id)
