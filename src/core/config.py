from envparse import Env

env = Env()


REAL_DB_URL: str = env.str(
    "REAL_DB_URL",
    default="postgresql+asyncpg://postgres:postgres@localhost:5433/todo",
)

ACCESS_TOKEN_EXPIRE_MINUTES: int = env.int(
    "ACCESS_TOKEN_EXPIRE_MINUTES",
    default=30,
)

ACCESS_TOKEN_ALGORITHM: str = env.str(
    "ACCESS_TOKEN_ALGORITHM",
    default="HS256",
)

ACCESS_TOKEN_SECRET_KEY: str = env.str(
    "ACCESS_TOKEN_SECRET_KEY",
    default="secret",
)
