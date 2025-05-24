from fastapi import HTTPException


async def NotAcceptableError(detail: str):
    raise HTTPException(status_code=406, detail=detail)
