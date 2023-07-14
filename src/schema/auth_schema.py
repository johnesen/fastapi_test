import uuid
from pydantic import BaseModel, EmailStr

from schema.base import TuneModel


class TokenSchema(BaseModel):
    access_token: str
    token_type: str
    
class SignInSchema(BaseModel):
    email: str
    password: str

class CodeVerification(BaseModel):
    code: str
    
    
class AuthResponse(TuneModel):
    user_id: uuid.UUID
    name: str
    surname: str
    email: EmailStr
    token: TokenSchema

