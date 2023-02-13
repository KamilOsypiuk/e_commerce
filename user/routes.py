from database import get_db
from user.model import User
from auth.schemas import UserOutput, UserUpdateInput
from user.password import hash_password
from auth.json_token import SECRET_KEY, ALGORITHM

from jose import jwt, JWTError
from sqlmodel import select, update

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer


router = APIRouter(tags=["user"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login", scheme_name="JWT")


async def get_current_user(
    token: str = Depends(oauth2_scheme), database=Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid Credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = read_user(email, database)
    if user is None:
        raise credentials_exception
    return user


def create_user(username, email, password, database):
    user = User(username=username, email=email, password=hash_password(password))
    database.add(user)
    database.commit()
    return UserOutput(id=user.id, email=user.email)


def read_user(email, database):
    statement = select(User).where(User.email == email).limit(1)
    user = database.scalar(statement)
    return user


@router.get(
    "/users/{id}/",
    status_code=status.HTTP_200_OK,
    response_description="Successfully fetched",
)
def read_one_user(id, database=Depends(get_db)):
    statement = select(User).where(User.id == id).limit(1)
    user = database.scalar(statement)
    return user


@router.get(
    "/users/",
    status_code=status.HTTP_200_OK,
    response_description="Successfully fetched",
)
def read_many_users(limit=None, offset=None, database=Depends(get_db)):
    statement = select(User).order_by(User.id).limit(limit).offset(offset)
    data = database.scalars(statement)
    results = data.all()
    return results


@router.put(
    "/users/",
    status_code=status.HTTP_200_OK,
    response_description="Successfully updated",
)
def update_user(
    update_fields: UserUpdateInput,
    database=Depends(get_db),
    user: User = Depends(get_current_user),
):
    statement = update(User).where(User.id == user.id).values(**update_fields.dict())
    database.execute(statement)
    database.commit()


@router.delete(
    "/users/",
    status_code=status.HTTP_204_NO_CONTENT,
    response_description="Successfully deleted",
)
def delete_user(database=Depends(get_db), user: User = Depends(get_current_user)):
    statement = select(User).where(User.id == user.id).limit(1)
    data = database.scalar(statement)
    if data is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Item not found"
        )
    database.delete(data)
    database.commit()
