from typing import Union

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

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login/token")


class AuthService:
    @staticmethod
    async def _get_user_by_email_for_auth(email: str, session: AsyncSession):
        async with session.begin():
            user_dal = UserDal(session)
            return await user_dal.get_user_by_email(
                email=email,
            )

    @classmethod
    async def authenticate_user(
        cls, email: str, password: str, db: AsyncSession
    ) -> Union[User, None]:
        user = await cls._get_user_by_email_for_auth(email=email, session=db)
        if user is None:
            raise HTTPException(status_code=404, detail="User does not exist")
        if not Hasher.verify_password(password, user.hashed_password):
            raise HTTPException(status_code=400, detail="Password is not correct")
        return user

    @classmethod
    async def get_current_user_from_token(
        cls, token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)
    ):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )
        try:
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
            )
            email: str = payload.get("sub")
            if email is None:
                raise credentials_exception
        except JWTError:
            raise credentials_exception
        user = await cls._get_user_by_email_for_auth(email=email, session=db)
        if user is None:
            raise credentials_exception
        return user
