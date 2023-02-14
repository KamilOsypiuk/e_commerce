from datetime import datetime, timedelta
import os
from jose import jwt
from uuid import uuid4


SECRET_KEY = os.environ["SECRET_KEY"]
REFRESH_SECRET_KEY = os.environ["REFRESH_SECRET_KEY"]
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 30


def create_access_token(subject: str) -> str:
    expire_time = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {
        "jti": str(uuid4()),
        "sub": subject,
        "exp": expire_time,
        "type": "access_token",
    }
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)
    return encoded_jwt


def create_refresh_token(subject: str) -> str:
    expire_time = datetime.utcnow() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    to_encode = {
        "jti": str(uuid4()),
        "sub": subject,
        "exp": expire_time,
        "type": "refresh_token",
    }
    encoded_jwt = jwt.encode(to_encode, REFRESH_SECRET_KEY, ALGORITHM)
    return encoded_jwt
