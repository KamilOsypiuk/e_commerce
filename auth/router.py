from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from auth.jwt import create_access_token, create_refresh_token
from database import get_db
from user.model import User
from user.password import verify_password
from user.schemas import TokenOutput, UserOutput, UserRegisterInput
from user.services import create_user, get_current_user, read_user_by_email

router = APIRouter(tags=["auth"])


@router.post(
    "/users/",
    status_code=status.HTTP_201_CREATED,
    response_description="Item have been created successfully",
    response_model=UserOutput,
)
def register_user(
        user: UserRegisterInput, database=Depends(get_db)
) -> UserOutput:
    if read_user_by_email(user.email, database=database) is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exist",
        )
    return create_user(user.username, user.email, user.fullname, user.password, database)


@router.post(
    "/login",
    status_code=status.HTTP_201_CREATED,
    response_description="You have been successfully logged in",
    response_model=TokenOutput,
)
def login(data: OAuth2PasswordRequestForm = Depends(), database=Depends(get_db)):
    if (user := read_user_by_email(email=data.username, database=database)) is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Credentials"
        )
    hashed_pass = user.password
    if not verify_password(data.password, hashed_pass):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Credentials"
        )
    return {
        "access_token": create_access_token(data.username),
        "refresh_token": create_refresh_token(data.username),
    }


@router.get(
    "/users/me",
    summary="Get details of currently logged in user",
    response_model=UserOutput,
)
def get_me(user: User = Depends(get_current_user)):
    return user
