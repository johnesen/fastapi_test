from typing import Union
from uuid import UUID

from fastapi import Depends
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from jose import JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from config import settings
from config.db_config import get_db
from config.hashing import Hasher
from dal import UserDal
from model import User
from schema.user_schema import ShowUser


class AuthService:
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/signin")

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
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
            )
            user_id: str = payload.get("user_id")
            if user_id is None:
                raise HTTPException(status_code=403, detail="Token not valid")
        except JWTError:
            raise HTTPException(status_code=403, detail="Token not valid or expired")
        user = await cls._get_user_by_id_for_auth(user_id=user_id, session=db)
        if user is None or not user.is_active:
            raise HTTPException(status_code=404, detail="User not found")
        return user
