from pydantic import EmailStr
from sqlmodel import Field
from sqlmodel import SQLModel

from ecommerce.User import hashing


class Users(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    username: str | None = None, Field(unique=True)
    email: EmailStr = Field(unique=True)
    password: str

    def __init__(self, username, email, password):
        super().__init__()
        self.username = username
        self.email = email
        self.password = hashing.get_hash_password(password)

    def check_password(self, password):
        return hashing.verify_password(self.password, password)
