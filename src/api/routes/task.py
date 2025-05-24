import uuid
from logging import getLogger

from api.errors.exceptions.Forbidden import ForbiddenError
from api.errors.functions.Database import DatabaseError
from api.errors.functions.NotAcceptable import NotAcceptableError
from api.errors.functions.NotFound import NotFoundErrorCheck
from api.errors.functions.Unprocessable import UnprocessableError
from core.dependencies.get_db import get_db
from db.models import Status
from db.models import User
from fastapi import APIRouter
from fastapi import Depends
from models.schemas.task import CreateTask
from models.schemas.task import DeletedTaskResponse
from models.schemas.task import RestoredTaskResponse
from models.schemas.task import ShowTask
from models.schemas.task import UpdatedTaskResponse
from models.schemas.task import UpdateTaskRequest
from services.auth import get_current_user_from_token
from services.task import _create_task
from services.task import _delete_task
from services.task import _get_authors
from services.task import _get_producers
from services.task import _get_task
from services.task import _restore_task
from services.task import _update_task
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from utils.task.is_user_active import is_user_active


task_router = APIRouter()


logger = getLogger(__name__)


@task_router.post("/", response_model=ShowTask)
async def create_task(
    body: CreateTask,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token),
) -> ShowTask:
    if not is_user_active(current_user.user_id, db):
        await NotAcceptableError("Author must be active.")
    try:
        task = await _create_task(author_id=current_user.user_id, body=body, session=db)
        return task
    except IntegrityError as err:
        logger.error(err)
        await DatabaseError(err)


@task_router.get("/", response_model=ShowTask)
async def get_task(
    task_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token),
) -> ShowTask:
    authors = await _get_authors(task_id=task_id, session=db)
    producers = await _get_producers(task_id=task_id, session=db)
    if current_user.user_id not in authors and current_user.user_id not in producers:
        raise ForbiddenError
    task = await _get_task(task_id=task_id, session=db)
    await NotFoundErrorCheck(task, "Task", task_id)
    return task


@task_router.patch("/", response_model=UpdatedTaskResponse)
async def update_task(
    task_id: uuid.UUID,
    body: UpdateTaskRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token),
) -> UpdatedTaskResponse:
    update_task_params = body.model_dump(exclude_none=True)
    if update_task_params == {}:
        await UnprocessableError("At least one parameter must be provided.")
    authors = await _get_authors(task_id=task_id, session=db)
    if current_user.user_id not in authors:
        raise ForbiddenError
    task = await _get_task(task_id=task_id, session=db)
    await NotFoundErrorCheck(task, "Task", task_id)
    updated_task_id = await _update_task(
        task_id=task_id, update_task_params=update_task_params, session=db
    )
    await NotFoundErrorCheck(updated_task_id, "Task", task_id)
    return UpdatedTaskResponse(updated_task_id=updated_task_id)


@task_router.patch("/status", response_model=UpdatedTaskResponse)
async def update_task_status(
    task_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token),
) -> UpdatedTaskResponse:
    task = await _get_task(task_id=task_id, session=db)
    await NotFoundErrorCheck(task, "Task", task_id)
    new_status = await task.next_status_level()
    authors = await _get_authors(task_id=task_id, session=db)
    producers = await _get_producers(task_id=task_id, session=db)
    if new_status == Status.Completed:
        if current_user.user_id in authors:
            await _update_task(
                task_id=task_id, update_task_params={"status": new_status}, session=db
            )
            deleted_task_id = await _delete_task(task_id=task_id, session=db)
            return UpdatedTaskResponse(updated_task_id=deleted_task_id)
        raise ForbiddenError
    if current_user.user_id not in authors and current_user.user_id not in producers:
        raise ForbiddenError
    updated_task_id = await _update_task(
        task_id=task_id, update_task_params={"status": new_status}, session=db
    )
    await NotFoundErrorCheck(updated_task_id, "Task", task_id)
    return UpdatedTaskResponse(updated_task_id=updated_task_id)


@task_router.delete("/", response_model=DeletedTaskResponse)
async def delete_task(
    task_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token),
) -> DeletedTaskResponse:
    authors = await _get_authors(task_id=task_id, session=db)
    if current_user.user_id not in authors:
        raise ForbiddenError
    deleted_task_id = await _delete_task(task_id=task_id, session=db)
    await NotFoundErrorCheck(deleted_task_id, "Task", task_id)
    return DeletedTaskResponse(deleted_task_id=deleted_task_id)


@task_router.post("/restore", response_model=RestoredTaskResponse)
async def restore_task(
    task_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token),
) -> DeletedTaskResponse:
    authors = await _get_authors(task_id=task_id, session=db)
    if current_user.user_id not in authors:
        raise ForbiddenError
    restored_task_id = await _restore_task(task_id=task_id, session=db)
    await NotFoundErrorCheck(restored_task_id, "Task", task_id)
    return RestoredTaskResponse(restored_task_id=restored_task_id)
