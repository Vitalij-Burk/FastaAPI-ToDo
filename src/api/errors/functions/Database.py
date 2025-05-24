from fastapi import HTTPException


async def DatabaseError(err):
    raise HTTPException(status_code=503, detail=f"Database error: {err}.")
