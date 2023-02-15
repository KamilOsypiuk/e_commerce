from pydantic import BaseModel, Field, EmailStr
from typing import Any
from user.password import hash_password


class UserOutput(BaseModel):
    id: int
    username: str = Field(default=None)
    email: str
    fullname: str = Field(default=None)
    created_at: Any


class UserRegisterInput(BaseModel):
    username: str = Field()
    email: EmailStr = Field()
    password: str = Field(min_length=6, max_length=30)
    fullname: str = Field()


class UserUpdateInput(UserRegisterInput):
    pass


class TokenOutput(BaseModel):
    access_token: str
    refresh_token: str
