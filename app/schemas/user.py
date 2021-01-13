from typing import Optional, Any

from pydantic import BaseModel, EmailStr, validator
from datetime import datetime


# Shared properties
class UserBase(BaseModel):
    username: Optional[str] = None
    name: Optional[str] = None


class UserCreate(UserBase):
    username: str
    name: str
    password: str
    site_id: int


class UserUpdate(UserBase):
    username: str
    name: str
    mobile: str
    password: Optional[str] = None


# Properties shared by models stored in DB
class UserInDBBase(UserBase):
    id: int
    disabled: int

    class Config:
        orm_mode = True


class User(UserInDBBase):
    pass


class UserOut(UserInDBBase):
    site_id: int
    is_mgmt: bool
    username: Optional[str] = None
    name: str
    mobile: Optional[str] = None
    email: Optional[str] = None
    avatar: Optional[str] = None
    created_at: Optional[datetime] = None

    # @validator('created_at')
    # def create_time_format(cls, v: Optional[datetime] = None):
    #     if v:
    #         return v.strftime("%Y-%m-%d %H:%M:%S")
    #     return ''
