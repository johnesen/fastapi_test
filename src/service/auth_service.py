from datetime import datetime, timedelta
from typing import Union
from uuid import UUID

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession

from config import ALGORITHM, SECRET_KEY, Hasher, get_db
from config.settings import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY
from dal import UserDal
from model import User
from model.user_model import User


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

    @classmethod
    async def veriify_by_code(cls, code: str, session) -> User:
        async with session.begin():
            user_dal = UserDal(session)
            user = await user_dal.verify_user_by_verify_code(code)
            if user is None:
                raise HTTPException(status_code=404, detail="User not found")
            return user
