from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import Response
from sqlmodel import select

from data.model import Data
from database import get_db
from user.model import User
from user.routes import get_current_user

router = APIRouter(tags=["data"])


@router.post(
    "/data/",
    status_code=status.HTTP_201_CREATED,
    response_description="Item have been created successfully",
)
def create_data(
        first_name: str,
        last_name: str,
        database=Depends(get_db),
        user: User = Depends(get_current_user),
) -> Response:
    database.add(Data(first_name=first_name, last_name=last_name, user_id=user.id))
    database.commit()
    return Response(status_code=status.HTTP_201_CREATED)


@router.get(
    "/data/{id}",
    status_code=status.HTTP_200_OK,
    response_description="Successfully fetched",
)
def get_data(
        id: int, database=Depends(get_db), user: User = Depends(get_current_user)
) -> Data:
    statement = select(Data).where(Data.id == id, Data.user_id == user.id).limit(1)
    data = database.scalar(statement)
    if data is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Item not found"
        )
    return data


@router.get(
    "/data/",
    status_code=status.HTTP_200_OK,
    response_description="Successfully fetched",
)
def get_many_data(
        limit: int = None,
        offset: int = None,
        database=Depends(get_db),
        user: User = Depends(get_current_user),
) -> list:
    statement = (
        select(Data)
        .where(Data.user_id == user.id)
        .limit(limit)
        .offset(offset)
    )
    data = database.scalars(statement)
    results = data.all()
    return results


@router.put(
    "/data/",
    status_code=status.HTTP_200_OK,
    response_description="Successfully updated",
)
def update_data(
        id: int,
        first_name: str,
        last_name: str,
        database=Depends(get_db),
        user: User = Depends(get_current_user),
) -> Response:
    statement = select(Data).where(Data.id == id, Data.user_id == user.id).limit(1)
    if statement is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Item not found"
        )
    data = database.scalar(statement)
    data.first_name = first_name
    data.last_name = last_name
    database.commit()
    return Response(status_code=status.HTTP_200_OK)


@router.delete(
    "/data/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_description="Successfully deleted",
)
def delete_data(
        id: int, database=Depends(get_db), user: User = Depends(get_current_user)
) -> Response:
    statement = select(Data).where(Data.id == id, Data.user_id == user.id).limit(1)
    data = database.scalar(statement)
    if data is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Item not found"
        )
    database.delete(data)
    database.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
