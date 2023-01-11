from pydantic import BaseModel, Field


class UserOut(BaseModel):
    id: str
    email: str


class UserAuth(BaseModel):
    username: str
    email: str
    password: str
