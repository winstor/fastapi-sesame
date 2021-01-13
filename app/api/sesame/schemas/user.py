from typing import Optional

from pydantic import BaseModel, EmailStr
from datetime import datetime


class UserCreate(BaseModel):
    username: str
    name: str
    password: str
    mobile: int


class UserUpdate(BaseModel):
    name: str
    mobile: str
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    qq: Optional[int] = None
    wechat_number: Optional[str] = None


class User(BaseModel):
    id: int

    class Config:
        orm_mode = True


class UserOut(User):
    username: Optional[str] = None
    name: str
    mobile: Optional[str] = None
    email: Optional[str] = None
    avatar: Optional[str] = None
    created_at: Optional[datetime] = None
