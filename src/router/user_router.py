from uuid import UUID
from fastapi import Depends
from fastapi.routing import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from config import get_db
from schema.user_schema import ShowDeletedUpdatedUser, ShowUser, UserCreate, UpdateUser
from service.user_service import UserService

user_router = APIRouter()


@user_router.post("/", response_model=ShowUser, status_code=201)
async def createUser(body: UserCreate, db: AsyncSession = Depends(get_db)) -> ShowUser:
    return await UserService.create_new_user(body, db)


@user_router.delete(
    "/{user_id}", response_model=ShowDeletedUpdatedUser, status_code=202
)
async def deleteUser(
    user_id: UUID, db: AsyncSession = Depends(get_db)
) -> ShowDeletedUpdatedUser:
    return await UserService.delete_user(user_id, db)


@user_router.get("/{user_id}", response_model=ShowUser, status_code=200)
async def getUserById(user_id: UUID, db: AsyncSession = Depends(get_db)) -> ShowUser:
    return await UserService.get_user_by_id(user_id, db)


@user_router.patch("/{user_id}", response_model=ShowDeletedUpdatedUser, status_code=200)
async def updateUserById(
    user_id: UUID, body: UpdateUser, db: AsyncSession = Depends(get_db)
) -> ShowUser:
    return await UserService.update_user_by_id(user_id=user_id, body=body, session=db)
