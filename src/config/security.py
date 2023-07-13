from datetime import timedelta, datetime
from jose import jwt

from model.user_model import User
from .settings import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY


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
