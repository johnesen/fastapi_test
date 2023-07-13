from pydantic import BaseModel


class TokenSchema(BaseModel):
    # user: dict
    access_token: str
    token_type: str
    
class SignInSchema(BaseModel):
    email: str
    password: str
