from typing import List, Optional, Any, Union
from fastapi import Depends
from datetime import datetime, timedelta
from jose import jwt
from pydantic import ValidationError
from fastapi import HTTPException, status
from fastapi.security import (
    OAuth2PasswordBearer,
    SecurityScopes,
)

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/login/access-token",
    # scopes={"me": "Read information about the current user.", "items": "Read items."},
)


class OAUTH:
    secret_key = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    algorithm = "HS256"
    expire_minutes = 3600 * 24

    def config(self, config: dict):
        if "secret_key" in config:
            self.secret_key = config.get("secret_key")
        if "algorithm" in config:
            self.algorithm = config.get("algorithm")
        if "expire_minutes" in config:
            self.expire_minutes = config.get("expire_minutes")

    def encode(self, data: dict, expires_delta: Optional[timedelta] = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=self.expire_minutes)
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)

    def decode(self, token: str = Depends(oauth2_scheme)):
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
        except (jwt.JWTError, ValidationError):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
            )
        return payload


oauth = OAUTH()
