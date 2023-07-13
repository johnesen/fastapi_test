from fastapi import Depends
from fastapi.routing import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from model import User
from config import get_db
from service import AuthService, UserService
from schema import ShowDeletedUpdatedUser, ShowUser, UserCreate, UpdateUser

user_router = APIRouter()


@user_router.post("/signup", response_model=ShowUser, status_code=201)
async def createUser(body: UserCreate, db: AsyncSession = Depends(get_db)) -> ShowUser:
    return await UserService.create_new_user(body, db)


@user_router.delete("/profile", response_model=ShowDeletedUpdatedUser, status_code=202)
async def deleteUser(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(AuthService.get_current_user_from_token),
) -> ShowDeletedUpdatedUser:
    return await UserService.delete_user(current_user.user_id, db)


@user_router.get("/profile", response_model=ShowUser, status_code=200)
async def getUserById(
    current_user: User = Depends(AuthService.get_current_user_from_token),
) -> ShowUser:
    return await UserService.get_user_by_id(current_user)


@user_router.patch("/profile", response_model=ShowDeletedUpdatedUser, status_code=200)
async def updateUserById(
    body: UpdateUser,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(AuthService.get_current_user_from_token),
) -> ShowUser:
    return await UserService.update_user_by_id(
        user_id=current_user.user_id, body=body, session=db
    )
