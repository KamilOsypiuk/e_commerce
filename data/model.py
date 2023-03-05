from sqlmodel import Field, SQLModel

from user.model import User


class Data(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    first_name: str
    last_name: str
    user_id: int = Field(default=None, foreign_key=User.id)
    title: str
