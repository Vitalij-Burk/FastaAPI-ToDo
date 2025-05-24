from fastapi import HTTPException


ForbiddenError = HTTPException(status_code=403, detail="Forbidden.")
