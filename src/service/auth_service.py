from typing import Union
from uuid import UUID

from fastapi import Depends
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession

from config import Hasher, get_db, ALGORITHM, SECRET_KEY
from dal import UserDal
from model import User


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
