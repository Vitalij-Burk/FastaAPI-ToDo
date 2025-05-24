from db.models import User
from services.user import _get_user_by_id
from sqlalchemy import UUID
from sqlalchemy.ext.asyncio import AsyncSession


async def is_user_active(user_id: UUID, session: AsyncSession):
    user: User = await _get_user_by_id(user_id=user_id, session=session)
    if not user.is_active_property():
        return False
    return True
