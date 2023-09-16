from typing import List, Union
from uuid import UUID

from config import Hasher
from fastapi import HTTPException
from model import User
from schema import ShowUser, UpdateUser, UserCreate
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from .send_email import SendEmailService


class UserService:
    @classmethod
    async def create_new_user(cls, body: UserCreate, session: AsyncSession) -> ShowUser:
        async with session.begin():
            query = select(User).where(User.email == body.email).limit(1)
            res = await session.execute(query)
            userExist = res.scalar()
            if userExist:
                raise HTTPException(
                    status_code=400, detail="User with this email alreay exist"
                )
            code = await SendEmailService.generate_code()
            new_user = User(
                name=body.name,
                surname=body.surname,
                email=body.email,
                hashed_password=Hasher.hash_password(body.password),
                code=code,
            )
            session.add(new_user)
            await session.commit()
            return new_user

    @classmethod
    async def get_all_users(cls, session: AsyncSession) -> List[ShowUser]:
        async with session.begin():
            query = select(User).where(User.is_active == True)
            res = await session.execute(query)
            users = res.scalars().all()
            await session.commit()
            return users

    @classmethod
    async def delete_user(cls, user_id, session: AsyncSession) -> dict:
        async with session.begin():
            try:
                query = (
                    update(User)
                    .where(User.user_id == user_id, User.is_active == True)
                    .values(is_active=False)
                )
                res = await session.execute(query)
                await session.commit()
                return True
            except:
                return False

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
        cls, user_id: UUID, body: UpdateUser, session: AsyncSession
    ) -> Union[UUID, None]:
        async with session.begin():
            update_data = body.dict(exclude_unset=True)
            query = (
                update(User)
                .where(User.user_id == user_id, User.is_active == True)
                .values(update_data)
                .returning(User)
            )
            res = await session.execute(query)
            user = res.scalar()
            if not user:
                raise HTTPException(
                    status_code=404, detail="User with this id not found"
                )
            return user
            return ShowUser(
                user_id=user.user_id,
                name=user.name,
                surname=user.surname,
                email=user.email,
                is_verified=user.is_verified,
            )
