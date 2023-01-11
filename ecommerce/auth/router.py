from fastapi import APIRouter, Depends, HTTPException, status
from .schemas import UserOut, UserAuth


from ecommerce.main import get_db
from ecommerce.User.model import Users
from ecommerce.main import create_user

router = APIRouter(tags=["auth"])


@router.post('/User/login')
def login():
    pass


@router.post('/sing_up/', response_model=UserOut)
async def register_user(data: UserAuth = Depends(get_db)):
    user = UserAuth.email
    if user in Users.email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exist")
    user = {
        'username': data.username,
        'email': data.email,
        'password': data.password}
    return create_user(user)


