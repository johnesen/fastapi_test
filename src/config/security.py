from datetime import timedelta, datetime
from functools import wraps
from jose import jwt

from model.user_model import User
from service.user_service import UserService

from . import settings


def create_access_token(user: User) -> str:
    data = {
        "user_id": str(user.user_id),
        "email": user.email,
        "name": f"{user.name} {user.surname}",
    }
    expires = datetime.utcnow() + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    data.update({"exp": expires, "iat": datetime.utcnow()})
    encoded_jwt = jwt.encode(data, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt