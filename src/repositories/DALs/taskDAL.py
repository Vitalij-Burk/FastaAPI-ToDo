import uuid

from db.models import Status
from db.models import Task
from db.models import User
from db.models import UserAssignedTask
from db.models import UserCreatedTask
from sqlalchemy import and_
from sqlalchemy import select
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession


class TaskDAL:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_task(
        self, author_id: uuid.UUID, producers_ids: list[uuid.UUID], task: str
    ):
        new_task = Task(task=task)
        author = await self.db_session.get(User, author_id)
        producers = [
            await self.db_session.get(User, producer_id)
            for producer_id in producers_ids
        ]

        if not author or not producers:
            raise ValueError("User not found")

        new_task.authors.append(UserCreatedTask(user=author, task=new_task))
        for producer in producers:
            new_task.producers.append(UserAssignedTask(user=producer, task=new_task))

        self.db_session.add(new_task)
        await self.db_session.flush()
        await self.db_session.refresh(new_task)
        return new_task

    async def update_task(self, task_id: uuid.UUID, **kwargs):
        query = (
            update(Task)
            .where(and_(Task.task_id == task_id, Task.is_active is True))
            .values(kwargs)
            .returning(Task.task_id)
        )
        res = await self.db_session.execute(query)
        updated_task_id_row = res.fetchone()
        if updated_task_id_row is not None:
            return updated_task_id_row[0]

    async def delete_task(self, task_id: uuid.UUID):
        query = (
            update(Task)
            .where(and_(Task.task_id == task_id, Task.is_active is True))
            .values(is_active=False)
            .returning(Task.task_id)
        )
        res = await self.db_session.execute(query)
        deleted_task_id = res.fetchone()
        if deleted_task_id is not None:
            return deleted_task_id[0]

    async def restore_task(self, task_id: uuid.UUID):
        query = (
            update(Task)
            .where(and_(Task.task_id == task_id, Task.is_active is False))
            .values(is_active=True, status=Status.Zero)
            .returning(Task.task_id)
        )
        res = await self.db_session.execute(query)
        deleted_task_id = res.fetchone()
        if deleted_task_id is not None:
            return deleted_task_id[0]

    async def get_task(self, task_id: uuid.UUID):
        query = select(Task).where(
            and_(Task.task_id == task_id, Task.is_active is True)
        )
        res = await self.db_session.execute(query)
        task_row = res.fetchone()
        if task_row is not None:
            return task_row[0]

    async def get_authors(self, task_id: uuid.UUID) -> list[uuid.UUID]:
        task = await self.db_session.get(Task, task_id)
        authors_ids = [author.user_id for author in task.authors]
        return authors_ids

    async def get_producers(self, task_id: uuid.UUID) -> list[uuid.UUID]:
        task = await self.db_session.get(Task, task_id)
        producers_ids = [producer.user_id for producer in task.producers]
        return producers_ids
