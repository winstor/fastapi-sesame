from datetime import datetime, timedelta
from typing import List, Optional, Any, Union
from jose import jwt
from passlib.context import CryptContext
from pydantic import ValidationError
from fastapi import HTTPException, status

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "a9d25e094faa6ca2556c818166b7a9563b93f7088f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 3600*24*30


def sign_encode(data: Union[str, int], expires_delta: Optional[timedelta] = None):
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    encoded_jwt = jwt.encode({
        "sub": str(data),
        "exp": expire
    }, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def sign_decode(auth_code: str):
    try:
        payload = jwt.decode(auth_code, SECRET_KEY, algorithms=[ALGORITHM])
        sub: str = payload.get("sub")
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )
    return sub
