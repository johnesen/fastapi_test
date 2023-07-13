from envparse import Env

env = Env()

DATABASE_URL: str = env.str(
    "DATABASE_URL",
    default="postgresql+asyncpg://db_user:db_password@0.0.0.0:5432/db_name",
)

SECRET_KEY: str = env.str("SECRET_KEY", default='secretkey')
ALGORITHM: str = env.str("ALGORITHM", default='HS256')
ACCESS_TOKEN_EXPIRE_MINUTES: int = env.str("ACCESS_TOKEN_EXPIRE_MINUTES", default=5)

MAIL_USERNAME: str = env.str("MAIL_USERNAME", default="nurjantunteev")
MAIL_PASSWORD: str = env.str("MAIL_PASSWORD", default="tspaggjoqtyhhtir")
MAIL_FROM: str = env.str("MAIL_FROM", default="nurjantunteev@gmail.com")
MAIL_PORT: int = env.int("MAIL_PORT", default=587)
MAIL_SERVER: str = env.str("MAIL_SERVER", default="smtp.gmail.com")
MAIL_FROM_NAME: str = env.str("MAIL_FROM_NAME", default="title")