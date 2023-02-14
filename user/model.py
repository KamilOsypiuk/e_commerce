from pydantic import EmailStr
from sqlmodel import Field
from sqlmodel import SQLModel
from datetime import datetime


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: int = Field(default=None, primary_key=True)
    username: str = Field(unique=True)
    email: EmailStr = Field(unique=True)
    password: str
    fullname: str = Field(default=None)
    created_at: datetime = Field(default=datetime.utcnow())
