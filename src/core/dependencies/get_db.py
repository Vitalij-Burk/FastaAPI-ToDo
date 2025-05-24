from typing import Generator

from db.session import async_session


async def get_db() -> Generator:
    try:
        async with async_session() as session:
            yield session
    finally:
        await session.close()
