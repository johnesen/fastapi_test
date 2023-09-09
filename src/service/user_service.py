from typing import List, Union
from uuid import UUID

from fastapi import BackgroundTasks, HTTPException

from config import Hasher
from dal import UserDal
from model import User
from schema import ShowDeletedUpdatedUser, ShowUser, UpdateUser, UserCreate

from .send_email import SendEmailService


class UserService:
    @classmethod
    async def create_new_user(cls, body: UserCreate, session) -> ShowUser:
        async with session.begin():
            user_dal = UserDal(session)
            user = await user_dal.create_user(
                name=body.name,
                surname=body.surname,
                email=body.email,
                hashed_password=Hasher.hash_password(body.password),
                code=await SendEmailService.generate_code(),
            )
            return user

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
    async def get_user_by_id(cls, user: User) -> Union[ShowUser, None]:
        return ShowUser(
            user_id=user.user_id,
            name=user.name,
            surname=user.surname,
            email=user.email,
        )

    @classmethod
    async def update_user_by_id(
        cls, user_id: UUID, body: UpdateUser, session
    ) -> Union[UUID, None]:
        async with session.begin():
            user_dal = UserDal(session)
            user = await user_dal.update_user(user_id, **body.dict())
            if user is None:
                raise HTTPException(
                    status_code=404, detail="User with this id not found"
                )
            return ShowDeletedUpdatedUser(user_id=user)
