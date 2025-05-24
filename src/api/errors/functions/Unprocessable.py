from fastapi import HTTPException


async def UnprocessableError(detail: str):
    raise HTTPException(status_code=422, detail=detail)
