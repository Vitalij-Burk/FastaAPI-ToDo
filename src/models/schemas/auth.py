from passlib.context import CryptContext
from pydantic import BaseModel


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Hasher:
    @staticmethod
    def verify_password(plain_pass: str, hashed_pass: str) -> bool:
        return pwd_context.verify(plain_pass, hashed_pass)

    @staticmethod
    def get_password_hash(plain_pass: str) -> str:
        return pwd_context.hash(plain_pass)


class Token(BaseModel):
    access_token: str
    token_type: str
