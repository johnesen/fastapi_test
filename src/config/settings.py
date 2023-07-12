from envparse import Env

env = Env()

DATABASE_URL: str = env.str(
    "DATABASE_URL",
    default="postgresql+asyncpg://db_user:db_password@0.0.0.0:5432/db_name",
)

SECRET_KEY: str = env.str("SECRET_KEY", default='secretkey')
ALGORITHM: str = env.str("ALGORITHM", default='HS256')
ACCESS_TOKEN_EXPIRE_MINUTES: int = env.str("ACCESS_TOKEN_EXPIRE_MINUTES", default=5)