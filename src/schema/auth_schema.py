from pydantic import BaseModel


class TokenSchema(BaseModel):
    access_token: str
    token_type: str


class SignInSchema(BaseModel):
    email: str
    password: str


class CodeVerification(BaseModel):
    code: str
