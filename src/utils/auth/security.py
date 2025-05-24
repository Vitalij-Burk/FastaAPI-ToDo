from datetime import datetime
from datetime import timedelta
from datetime import timezone
from typing import Optional

from core.config import ACCESS_TOKEN_ALGORITHM
from core.config import ACCESS_TOKEN_EXPIRE_MINUTES
from core.config import ACCESS_TOKEN_SECRET_KEY
from jose import jwt


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, ACCESS_TOKEN_SECRET_KEY, algorithm=ACCESS_TOKEN_ALGORITHM
    )
    return encoded_jwt
