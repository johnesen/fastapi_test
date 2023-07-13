from typing import List, Union
from fastapi import HTTPException
from sqlalchemy import select, update, insert
from sqlalchemy.ext.asyncio import AsyncSession
from model.user_model import User
from uuid import UUID


class UserDal:
    def __init__(self, db_session: AsyncSession) -> None:
        self.db_session = db_session

    async def delete_user(self, user_id: UUID) -> Union[UUID, None]:
        query = (
            update(User)
            .where(User.user_id == user_id, User.is_active == True)
            .values(is_active=False)
            .returning(User.user_id)
        )
        res = await self.db_session.execute(query)
        deleted_user_id_row = res.fetchone()
        if deleted_user_id_row is not None:
            return deleted_user_id_row[0]

    async def get_user_by_id(self, user_id: UUID) -> User:
        query = select(User).where(User.user_id == user_id)
        res = await self.db_session.execute(query)
        user_row = res.fetchone()
        if user_row is not None:
            return user_row[0]

    async def get_user_by_email(self, email: str) -> User:
        query = select(User).where(User.email == email)
        res = await self.db_session.execute(query)
        user_row = res.fetchone()
        if user_row is not None:
            return user_row[0]
