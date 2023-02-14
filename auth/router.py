from fastapi.security import OAuth2PasswordRequestForm
from fastapi import HTTPException, status, Depends, APIRouter


from database import get_db
from user.model import User
from user.routes import create_user, read_user, get_current_user
from user.password import verify_password
from auth.schemas import UserOutput, UserRegisterInput, TokenOutput
from auth.json_token import create_access_token, create_refresh_token

router = APIRouter(tags=["auth"])


@router.post(
    "/users/",
    status_code=status.HTTP_201_CREATED,
    response_description="Item have been created successfully",
    response_model=UserOutput,
)
async def register_user(
    data: UserRegisterInput, database=Depends(get_db)
) -> UserOutput:
    if (user := read_user(data.email, database=database)) is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exist",
        )
    return create_user(data.username, data.email, data.password, database=database)


@router.post(
    "/login",
    status_code=status.HTTP_201_CREATED,
    response_description="You have been successfully logged in",
    response_model=TokenOutput,
)
async def login(data: OAuth2PasswordRequestForm = Depends(), database=Depends(get_db)):
    if (user := read_user(email=data.username, database=database)) is None:
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
async def get_me(user: User = Depends(get_current_user)):
    return user
