from decouple import config

DATABASE_URL: str = config("DATABASE_URL")
DATABASE_URL_ALEMBIC: str = config("DATABASE_URL_ALEMBIC")

SECRET_KEY: str = config("SECRET_KEY", default="secretkey")
ALGORITHM: str = config("ALGORITHM", default="HS256")
ACCESS_TOKEN_EXPIRE_MINUTES: int = config(
    "ACCESS_TOKEN_EXPIRE_MINUTES", cast=int, default=30
)

MAIL_USERNAME: str = config("MAIL_USERNAME")
MAIL_PASSWORD: str = config("MAIL_PASSWORD")
MAIL_FROM: str = config("MAIL_FROM")
MAIL_PORT: int = config("MAIL_PORT", cast=int)
MAIL_SERVER: str = config("MAIL_SERVER")
MAIL_FROM_NAME: str = config("MAIL_FROM_NAME")
