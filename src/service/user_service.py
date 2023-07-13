from typing import List, Union
from uuid import UUID
from fastapi import HTTPException
from sqlalchemy import insert, select, update

from dal.user_db_service import UserDal
from model.user_model import User
from schema.user_schema import (
    ShowDeletedUpdatedUser,
    UpdateUser,
    ShowUser,
    UserCreateBodySchema,
    UserCreateSchema,
)
from config.hashing import Hasher
from config.db_config import database


def get_user_service():
    return UserService(database)


class UserService:
    def __init__(self, database) -> None:
        self.database = database

    @classmethod
    async def get_all_users(cls, session) -> List[ShowUser]:
        async with session.begin():
            user_dal = UserDal(session)
            users = await user_dal.get_users()

    @classmethod
    async def delete_user(cls, user_id, session) -> Union[UUID, None]:
        async with session.begin():
            user_dal = UserDal(session)
            deleted_user_id = await user_dal.delete_user(user_id)
            if deleted_user_id is None:
                raise HTTPException(
                    status_code=404, detail="User with this id not found"
                )
            return ShowDeletedUpdatedUser(user_id=deleted_user_id)

    @classmethod
    async def get_user_by_id(cls, user_id: UUID, session) -> Union[ShowUser, None]:
        async with session.begin():
            user_dal = UserDal(session)
            user = await user_dal.get_user_by_id(user_id)
            if user is None:
                raise HTTPException(
                    status_code=404, detail="User with this id not found"
                )
            return user

    async def get_user_by_id(self, user_id: UUID) -> Union[ShowUser, None]:
        query = select(User).where(User.user_id == user_id)
        user = await self.database.execute(query)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return {"user_id": user}

    async def create(self, body: UserCreateBodySchema) -> UserCreateSchema:
        query = select(User).where(User.email == body.email)
        user_exist = await self.database.execute(query)
        if user_exist:
            raise HTTPException(
                status_code=400, detail="User with this email alreay exist"
            )
        user = UserCreateSchema(
            name=body.name,
            surname=body.surname,
            email=body.email,
            hashed_password=Hasher.hash_password(body.password),
        )
        query = insert(User).values(user.dict())
        await self.database.execute(query)
        return user

    async def update(self, user_id: UUID, body: UpdateUser) -> ShowDeletedUpdatedUser:
        query = (
            select(User).where(User.email == body.email).where(User.user_id != user_id)
        )
        user_exist = await self.database.execute(query)
        print(user_exist)
        if user_exist:
            raise HTTPException(
                status_code=400,
                detail="User with this email alreay exist, please choose another email",
            )
        user = UpdateUser(**body.dict())
        query = (
            update(User)
            .where(User.user_id == user_id)
            .values(user.dict())
            .returning(User)
        )
        user = await self.database.execute(query)
        return {"user_id": user}
