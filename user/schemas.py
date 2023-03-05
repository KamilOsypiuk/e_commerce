from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class UserOutput(BaseModel):
    id: int
    username: str | None = None
    email: str
    fullname: str | None = None
    created_at: datetime

    class Config:
        orm_mode = True


class UserRegisterInput(BaseModel):
    username: str
    email: EmailStr
    password: str = Field(min_length=6, max_length=30)
    fullname: str


class UserUpdateInput(UserRegisterInput):
    pass


class TokenOutput(BaseModel):
    access_token: str
    refresh_token: str
