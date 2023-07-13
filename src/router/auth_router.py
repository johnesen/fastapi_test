from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from model import User
from service import AuthService
from schema import SignInSchema, TokenSchema
from config import get_db
from service.auth_service import create_access_token

login_router = APIRouter()


@login_router.post("/signin", response_model=TokenSchema, status_code=200)
async def signin(body: SignInSchema, db: AsyncSession = Depends(get_db)) -> TokenSchema:
    user = await AuthService.authenticate_user(body.email, body.password, db)
    access_token = create_access_token(user=user)
    return TokenSchema(access_token=access_token, token_type="Bearer")


@login_router.get("/profile", status_code=200)
async def signin(current_user: User = Depends(AuthService.get_current_user_from_token)):
    return current_user
