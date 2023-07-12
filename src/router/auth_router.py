from datetime import timedelta

from fastapi import APIRouter
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from config.db_config import get_db
from config.security import create_access_token
from service import AuthService
from schema.auth_schema import TokenSchema

login_router = APIRouter()


@login_router.post("/signin", response_model=TokenSchema, status_code=200)
async def signin(
    form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)
) -> TokenSchema:
    user = await AuthService.authenticate_user(
        form_data.username,
        form_data.password,
        db,
    )
    access_token = create_access_token(user=user)
    return TokenSchema(access_token=access_token, token_type="Bearer")
