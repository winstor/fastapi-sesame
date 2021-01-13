import time
from typing import Optional
from pydantic import BaseModel, validator


class FileBase(BaseModel):
    name: str
    path: str
    type: str
    size: str


class FileCreate(FileBase):
    site_id: int
    user_id: int
    date: int


class FileUpdate(FileBase):
    pass


# Properties shared by models stored in DB
class FileInDBBase(FileBase):
    id: int

    class Config:
        orm_mode = True


class File(FileBase):
    pass


class FileOut(FileInDBBase):
    name: str
    path: str
    type: Optional[str] = None
    size: Optional[int] = None
    date: Optional[int] = None

    @validator('date')
    def create_time_format(cls, date: Optional[int] = None):
        if date:
            time_array = time.localtime(date)
            date = time.strftime("%Y--%m--%d %H:%M:%S", time_array)
            return date
        return ''
