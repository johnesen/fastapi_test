from __future__ import annotations

import re
import uuid

from fastapi import HTTPException
from pydantic import BaseModel, EmailStr, constr, validator

from schema.base import TuneModel

LETTER_MATCH_PATTERN = re.compile(r"^[a-zA-Z\-]+$")


class ShowUser(TuneModel):
    user_id: uuid.UUID
    name: str
    surname: str
    email: EmailStr
    is_verified: bool


class UpdateUser(BaseModel):
    name: (constr(min_length=1) | None)
    surname: (constr(min_length=1) | None)
    email: (EmailStr | None)


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
