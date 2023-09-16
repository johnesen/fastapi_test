from typing import List

from config import get_db
from fastapi import BackgroundTasks, Depends
from fastapi.routing import APIRouter
from model import User
from schema import ShowUser, UpdateUser, UserCreate
from service import AuthService, SendEmailService, UserService
from sqlalchemy.ext.asyncio import AsyncSession

user_router = APIRouter()


@user_router.post("/signup", status_code=201)
async def createUser(
    body: UserCreate,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
) -> dict:
    user = await UserService.create_new_user(body, db)
    SendEmailService.send_email_background(
        background_tasks,
        "Verification",
        user.email,
        f"your code: {user.code}",
    )
    return {"message": f"{user.email} registered successfullly and code sent to email"}


@user_router.delete("/profile", status_code=204)
async def deleteUser(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(AuthService.get_current_user_from_token),
) -> None:
    await UserService.delete_user(current_user.user_id, db)


@user_router.get("/profile", response_model=ShowUser, status_code=200)
async def getUserById(
    current_user: User = Depends(AuthService.get_current_user_from_token),
) -> ShowUser:
    return current_user


@user_router.patch("/profile", response_model=ShowUser, status_code=200)
async def updateUserById(
    body: UpdateUser,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(AuthService.get_current_user_from_token),
) -> ShowUser:
    return await UserService.update_user_by_id(
        user_id=current_user.user_id, body=body, session=db
    )


@user_router.get("/list", response_model=List[ShowUser], status_code=200)
async def updateUserById(
    db: AsyncSession = Depends(get_db),
) -> List[ShowUser]:
    user = await UserService.get_all_users(db)
    return user
