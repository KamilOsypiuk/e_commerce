from sqlmodel import SQLModel, Field
from ecommerce.User.model import Users


class Data(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    first_name: str
    last_name: str
    user_id: str = Field(default=None, foreign_key=Users.id)
