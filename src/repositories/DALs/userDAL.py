import uuid

from db.models import User
from sqlalchemy import and_
from sqlalchemy import select
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession


class UserDAL:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_user(
        self, username: str, email: str, hashed_password: str
    ) -> User:
        new_user = User(username=username, email=email, hashed_password=hashed_password)
        self.db_session.add(new_user)
        await self.db_session.flush()
        await self.db_session.refresh(new_user, ["created_tasks", "assigned_tasks"])
        return new_user

    async def update_user(self, user_id: uuid.UUID, **kwargs) -> uuid.UUID:
        query = (
            update(User)
            .where(and_(User.user_id == user_id, User.is_active is True))
            .values(kwargs)
            .returning(User.user_id)
        )
        res = await self.db_session.execute(query)
        updated_user_id_row = res.fetchone()
        if updated_user_id_row is not None:
            return updated_user_id_row[0]

    async def delete_user(self, user_id: uuid.UUID) -> uuid.UUID:
        query = (
            update(User)
            .where(and_(User.user_id == user_id, User.is_active is True))
            .values(is_active=False)
            .returning(User.user_id)
        )
        res = await self.db_session.execute(query)
        deleted_user_id = res.fetchone()
        if deleted_user_id is not None:
            return deleted_user_id[0]

    async def get_user_by_id(self, user_id: uuid.UUID) -> User:
        query = select(User).where(
            and_(User.user_id == user_id, User.is_active is True)
        )
        res = await self.db_session.execute(query)
        user_row = res.fetchone()
        if user_row is not None:
            return user_row[0]

    async def get_user_by_email(self, email: str) -> User:
        query = select(User).where(and_(User.email == email, User.is_active is True))
        res = await self.db_session.execute(query)
        user_row = res.fetchone()
        if user_row is not None:
            return user_row[0]

    async def get_created_tasks(self, user_id: uuid.UUID) -> list[uuid.UUID]:
        user = await self.db_session.get(User, user_id)
        created_tasks_ids = [
            created_task.task_id for created_task in user.created_tasks
        ]
        return created_tasks_ids

    async def get_assigned_tasks(self, user_id: uuid.UUID) -> list[uuid.UUID]:
        user = await self.db_session.get(User, user_id)
        assigned_tasks_ids = [
            assigned_task.task_id for assigned_task in user.assigned_tasks
        ]
        return assigned_tasks_ids
