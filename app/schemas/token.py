from typing import Optional, List,Any
from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None
    scopes: Optional[List[str]] = None


class TokenPayload(BaseModel):
    sub: Optional[str] = None
    site_id: Optional[int] = None
    nickname: Optional[str] = None
    exp: Optional[Any] = None
