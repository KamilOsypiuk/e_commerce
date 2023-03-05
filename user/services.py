from typing import Any

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlmodel import select

from auth.jwt import ALGORITHM, SECRET_KEY
from database import get_db
from user.model import User
from user.password import hash_password
from user.schemas import UserOutput

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login", scheme_name="JWT")


def get_current_user(
        token: str = Depends(oauth2_scheme), database=Depends(get_db)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid Credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    if (user := read_user_by_email(email, database)) is None:
        raise credentials_exception
    return user


def create_user(username: str, email: str, fullname: str, password: str, database) -> UserOutput:
    user = User(username=username, email=email, fullname=fullname, password=hash_password(password))
    database.add(user)
    database.commit()
    return UserOutput(user)


def read_user_by_email(email: str, database) -> User:
    statement = select(User).where(User.email == email).limit(1)
    user = database.scalar(statement)
    return user
