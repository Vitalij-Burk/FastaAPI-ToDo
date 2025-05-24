import uuid
from typing import Union

from db.models import User
from models.schemas.auth import Hasher
from models.schemas.user import CreateUser
from models.schemas.user import ShowUser
from repositories.DALs.userDAL import UserDAL
from sqlalchemy.ext.asyncio import AsyncSession


async def _create_user(body: CreateUser, session: AsyncSession) -> ShowUser:
    async with session.begin():
        user_dal = UserDAL(session)
        user: User = await user_dal.create_user(
            username=body.username,
            email=body.email,
            hashed_password=Hasher.get_password_hash(body.password),
        )
        return ShowUser(
            user_id=user.user_id,
            username=user.username,
            email=user.email,
            is_active=user.is_active,
        )


async def _update_user(
    user_id: uuid.UUID, update_user_params: dict, session: AsyncSession
) -> Union[uuid.UUID, None]:
    async with session.begin():
        user_dal = UserDAL(session)
        updated_user_id = await user_dal.update_user(
            user_id=user_id, **update_user_params
        )
        return updated_user_id


async def _get_user_by_id(
    user_id: uuid.UUID, session: AsyncSession
) -> Union[User, None]:
    async with session.begin():
        user_dal = UserDAL(session)
        user: User = await user_dal.get_user_by_id(user_id=user_id)
        if user is not None:
            return user


async def _get_created_tasks(
    user_id: uuid.UUID, session: AsyncSession
) -> list[uuid.UUID]:
    async with session.begin():
        user_dal = UserDAL(session)
        created_tasks = await user_dal.get_created_tasks(user_id=user_id)
        if created_tasks is None:
            return []
        return created_tasks


async def _get_assigned_tasks(
    user_id: uuid.UUID, session: AsyncSession
) -> list[uuid.UUID]:
    async with session.begin():
        user_dal = UserDAL(session)
        assigned_tasks = await user_dal.get_assigned_tasks(user_id=user_id)
        if assigned_tasks is None:
            return []
        return assigned_tasks


async def _delete_user(
    user_id: uuid.UUID, session: AsyncSession
) -> Union[uuid.UUID, None]:
    async with session.begin():
        user_dal = UserDAL(session)
        deleted_user_id = await user_dal.delete_user(user_id=user_id)
        return deleted_user_id
