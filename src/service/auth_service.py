import random
from typing import Union
from uuid import UUID

from fastapi import Depends
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession

from config import Hasher, get_db, ALGORITHM, SECRET_KEY
from config.settings import (
    MAIL_FROM,
    MAIL_FROM_NAME,
    MAIL_PASSWORD,
    MAIL_PORT,
    MAIL_SERVER,
    MAIL_USERNAME,
)
from dal import UserDal
from model import User


from datetime import timedelta, datetime
from jose import jwt

from model.user_model import User
from config.settings import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY


def create_access_token(user: User) -> str:
    data = {
        "user_id": str(user.user_id),
        "email": user.email,
        "name": f"{user.name} {user.surname}",
    }
    expires = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    data.update({"exp": expires, "iat": datetime.utcnow()})
    encoded_jwt = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


class AuthService:
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/signin")

    @staticmethod
    async def _get_user_by_id_for_auth(user_id: UUID, session: AsyncSession):
        async with session.begin():
            user_dal = UserDal(session)
            return await user_dal.get_user_by_id(user_id=user_id)

    @staticmethod
    async def _get_user_by_email_for_auth(email: str, session: AsyncSession):
        async with session.begin():
            user_dal = UserDal(session)
            return await user_dal.get_user_by_email(email=email)

    @classmethod
    async def authenticate_user(
        cls, email: str, password: str, db: AsyncSession
    ) -> Union[User, None]:
        user = await cls._get_user_by_email_for_auth(email=email, session=db)
        if user is None or not user.is_active:
            raise HTTPException(status_code=404, detail="User not found")
        if not Hasher.verify_password(password, user.hashed_password):
            raise HTTPException(status_code=400, detail="Password is not correct")
        return user

    @classmethod
    async def get_current_user_from_token(
        cls, token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)
    ):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            user_id: str = payload.get("user_id")
            if user_id is None:
                raise HTTPException(status_code=403, detail="Token not valid")
        except JWTError:
            raise HTTPException(status_code=403, detail="Token not valid or expired")
        user = await cls._get_user_by_id_for_auth(user_id=user_id, session=db)
        if user is None or not user.is_active:
            raise HTTPException(status_code=404, detail="User not found")
        return user


class SendEmailService:
    conf = ConnectionConfig(
        MAIL_USERNAME=MAIL_USERNAME,
        MAIL_PASSWORD=MAIL_PASSWORD,
        MAIL_FROM=MAIL_FROM,
        MAIL_PORT=MAIL_PORT,
        MAIL_SERVER=MAIL_SERVER,
        MAIL_FROM_NAME=MAIL_FROM_NAME,
        MAIL_STARTTLS=True,
        MAIL_SSL_TLS=False,
        USE_CREDENTIALS=True,
        # TEMPLATE_FOLDER='./templates/email'
    )

    @classmethod
    async def send_email(cls, email_to: str, body: str, subject: str):
        message = MessageSchema(
            subject=subject,
            recipients=[email_to],
            body=body,
            subtype="html",
        )

        fm = FastMail(cls.conf)
        await fm.send_message(
            message,
            # template_name="email.html",
        )

    @staticmethod
    async def generate_code():
        digit = str(random.randint(1, 999_999))
        code = digit if len(digit) == 6 else "0" * (6 - len(digit)) + digit
        return code
