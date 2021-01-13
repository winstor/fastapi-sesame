from typing import Optional
from pydantic import BaseModel


class FieldCateCreate(BaseModel):
    field_cname: str
    slug: str
    type: int = 1


class FieldCateUpdate(FieldCateCreate):
    pass


class FieldCate(BaseModel):
    id: int
    field_cname: str
    slug: str
    type: int

    class Config:
        orm_mode = True
