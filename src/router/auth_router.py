from config import get_db
from fastapi import APIRouter, Depends
from schema import CodeVerification, SignInSchema, TokenSchema
from service import AuthService, create_access_token
from sqlalchemy.ext.asyncio import AsyncSession

login_router = APIRouter()


@login_router.post("/signin", response_model=TokenSchema, status_code=200)
async def signin(body: SignInSchema, db: AsyncSession = Depends(get_db)) -> TokenSchema:
    user = await AuthService.authenticate_user(body.email, body.password, db)
    access_token = create_access_token(user=user)
    return TokenSchema(access_token=access_token, token_type="Bearer")


@login_router.post("/verify", response_model=TokenSchema, status_code=200)
async def signin(
    body: CodeVerification, db: AsyncSession = Depends(get_db)
) -> TokenSchema:
    verified = await AuthService.veriify_by_code(body.code, db)
    access_token = create_access_token(user=verified)
    return TokenSchema(access_token=access_token, token_type="Bearer")
