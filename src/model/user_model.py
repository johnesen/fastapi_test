import uuid

from config.db_config import Base
from sqlalchemy import Boolean, Column, String
from sqlalchemy.dialects.postgresql import UUID


class User(Base):
    __tablename__ = "users"

    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    hashed_password = Column(String, nullable=True)
    code = Column(String, nullable=True)
    is_verified = Column(Boolean(), default=False)
    is_active = Column(Boolean(), default=True)
