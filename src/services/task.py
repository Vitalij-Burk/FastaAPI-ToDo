import uuid
from typing import Union

from db.models import Task
from models.schemas.task import CreateTask
from models.schemas.task import ShowTask
from repositories.DALs.taskDAL import TaskDAL
from sqlalchemy.ext.asyncio import AsyncSession


async def _create_task(
    author_id: uuid.UUID, body: CreateTask, session: AsyncSession
) -> ShowTask:
    async with session.begin():
        task_dal = TaskDAL(session)
        task: Task = await task_dal.create_task(
            author_id=author_id, producers_ids=body.producers_ids, task=body.task
        )
        return ShowTask(
            task_id=task.task_id,
            task=task.task,
            status=task.status,
        )


async def _update_task(
    task_id: uuid.UUID, update_task_params: dict, session: AsyncSession
) -> Union[uuid.UUID, None]:
    async with session.begin():
        task_dal = TaskDAL(session)
        updated_task_id = await task_dal.update_task(task_id, **update_task_params)
        return updated_task_id


async def _get_task(task_id: uuid.UUID, session: AsyncSession) -> Union[Task, None]:
    async with session.begin():
        task_dal = TaskDAL(session)
        task: Task = await task_dal.get_task(task_id)
        if task is not None:
            return task


async def _get_authors(task_id: uuid.UUID, session: AsyncSession) -> list[uuid.UUID]:
    async with session.begin():
        task_dal = TaskDAL(session)
        authors = await task_dal.get_authors(task_id)
        if authors is None:
            return []
        return authors


async def _get_producers(task_id: uuid.UUID, session: AsyncSession) -> list[uuid.UUID]:
    async with session.begin():
        task_dal = TaskDAL(session)
        producers = await task_dal.get_producers(task_id)
        if producers is None:
            return []
        return producers


async def _delete_task(
    task_id: uuid.UUID, session: AsyncSession
) -> Union[uuid.UUID, None]:
    async with session.begin():
        task_dal = TaskDAL(session)
        deleted_task_id = await task_dal.delete_task(task_id)
        return deleted_task_id


async def _restore_task(
    task_id: uuid.UUID, session: AsyncSession
) -> Union[uuid.UUID, None]:
    async with session.begin():
        task_dal = TaskDAL(session)
        restored_task_id = await task_dal.restore_task(task_id)
        return restored_task_id
