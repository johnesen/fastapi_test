from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Hasher:
    @staticmethod
    def verify_password(password: str, hashed_password: str) -> str:
        return pwd_context.verify(password, hashed_password)
    

    @staticmethod
    def hash_password(password: str) -> str:
        return pwd_context.hash(password)