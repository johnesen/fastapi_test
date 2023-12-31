from typing import Annotated

from fastapi import BackgroundTasks, Depends
from fastapi.routing import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from config import get_db
from model import User
from schema import ShowUser, UpdateUser, UserCreate
from service import AuthService, SendEmailService, UserService

user_router = APIRouter()
currentUser = Annotated[User, Depends(AuthService.get_current_user_from_token)]


@user_router.post("/signup", status_code=201)
async def createUser(
    body: UserCreate,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
) -> dict:
    user = await UserService.create(body, db)
    SendEmailService.send_email_background(
        background_tasks,
        "Verification",
        user.email,
        f"your code: {user.code}",
    )
    return {"message": f"{user.email} registered successfullly and code sent to email"}


@user_router.delete("/profile", status_code=204)
async def deleteUser(
    current_user: currentUser, db: AsyncSession = Depends(get_db)
) -> None:
    await UserService.delete(current_user.user_id, db)


@user_router.get("/profile", response_model=ShowUser, status_code=200)
async def profile(current_user: currentUser) -> ShowUser:
    return current_user


@user_router.patch("/profile", response_model=ShowUser, status_code=200)
async def updateUser(
    body: UpdateUser, current_user: currentUser, db: AsyncSession = Depends(get_db)
) -> ShowUser:
    return await UserService.update(user_id=current_user.user_id, body=body, session=db)


@user_router.get("/list", response_model=list[ShowUser], status_code=200)
async def getUsers(db: AsyncSession = Depends(get_db)):
    user: list[ShowUser] = await UserService.get_users(db)
    return user
