import datetime
import re
import uuid
from typing import Optional
from fastapi import HTTPException
from pydantic import BaseModel, EmailStr, constr, validator


LETTER_MATCH_PATTERN = re.compile(r"^[a-zA-Z\-]+$")


class TuneModel(BaseModel):
    class Config:
        orm_mode = True


class ShowUser(TuneModel):
    user_id: uuid.UUID
    name: str
    surname: str
    email: EmailStr
    is_active: bool


class ShowDeletedUpdatedUser(BaseModel):
    user_id: uuid.UUID


class UpdateUser(BaseModel):
    name: Optional[constr(min_length=1)]
    surname: Optional[constr(min_length=1)]
    email: Optional[EmailStr]

class user(BaseModel):
    user_id: uuid.UUID
    name: str
    surname: str
    email: EmailStr
    is_active: bool
    hashed_password: str

class UserCreate(BaseModel):
    name: str
    surname: str
    email: EmailStr
    password: str

    @validator("name")
    def validate_name(cls, value):
        if not LETTER_MATCH_PATTERN.match(value):
            raise HTTPException(
                status_code=400, detail="Name should contain only latin letters"
            )

        return value

    @validator("surname")
    def validate_surname(cls, value):
        if not LETTER_MATCH_PATTERN.match(value):
            raise HTTPException(
                status_code=400, detail="surname should contain only latin letters"
            )

        return value
