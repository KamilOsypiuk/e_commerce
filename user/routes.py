from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import Response
from sqlmodel import select, update

from database import get_db
from user.model import User
from user.password import hash_password
from user.schemas import UserOutput, UserUpdateInput
from user.services import get_current_user

router = APIRouter(tags=["user"])


@router.get(
    "/users/{id}",
    status_code=status.HTTP_200_OK,
    response_description="Successfully fetched",
    response_model=UserOutput
)
def read_one_user(id: int, database=Depends(get_db)) -> UserOutput:
    if (statement := select(User).where(User.id == id).limit(1)) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    user = database.scalar(statement)
    return user


@router.get(
    "/users/",
    status_code=status.HTTP_200_OK,
    response_description="Successfully fetched",
)
def read_many_users(limit: int = None, offset: int = None, database=Depends(get_db)) -> list:
    statement = select(User).limit(limit).offset(offset)
    data = database.scalars(statement)
    results = data.all()
    return results


@router.put(
    "/users/",
    status_code=status.HTTP_200_OK,
    response_description="Successfully updated",
    response_model=UserOutput
)
def update_user(
        update_fields: UserUpdateInput,
        database=Depends(get_db),
        user: User = Depends(get_current_user),
) -> User:
    update_fields.password = hash_password(update_fields.password)
    statement = update(User).where(User.id == user.id).values(**update_fields.dict())
    database.execute(statement)
    database.commit()
    return user


@router.delete(
    "/users/",
    status_code=status.HTTP_204_NO_CONTENT,
    response_description="Successfully deleted",
)
def delete_user(database=Depends(get_db), user: User = Depends(get_current_user)) -> Response:
    statement = select(User).where(User.id == user.id).limit(1)
    data = database.scalar(statement)
    database.delete(data)
    database.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
