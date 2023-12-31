from __future__ import annotations

from uuid import UUID

from fastapi import HTTPException
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from config import Hasher
from model import User
from schema import ShowUser, UpdateUser, UserCreate

from .send_email import SendEmailService


class UserService:
    @classmethod
    async def create(cls, body: UserCreate, session: AsyncSession) -> ShowUser:
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
    async def get_users(cls, session: AsyncSession):
        async with session.begin():
            query = select(User).where(User.is_active == True)
            res = await session.execute(query)
            users = res.scalars().all()
            await session.commit()
            return users

    @classmethod
    async def delete(cls, user_id, session: AsyncSession) -> dict:
        async with session.begin():
            try:
                query = (
                    update(User)
                    .where(User.user_id == user_id, User.is_active == True)
                    .values(is_active=False)
                )
                await session.execute(query)
                await session.commit()
                return True
            except Exception:
                return False

    @classmethod
    async def update(
        cls, user_id: UUID, body: UpdateUser, session: AsyncSession
    ) -> (UUID | None):
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
