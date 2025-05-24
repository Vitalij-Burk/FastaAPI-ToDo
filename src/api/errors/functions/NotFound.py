import uuid

from fastapi import HTTPException


async def NotFoundErrorCheck(obj, name: str, id: uuid.UUID):
    if obj is None:
        raise HTTPException(
            status_code=404, detail=f"{name.capitalize()} with id {id} not found."
        )
