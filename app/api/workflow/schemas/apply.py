from typing import Optional
from pydantic import BaseModel


class ApplyCreate(BaseModel):
    title: str
    data: dict


class ApplyStore(ApplyCreate):
    site_id: int
    workflow_id: int
    creator_id: int
    create_user: str


class Apply(BaseModel):
    id: int

    class Config:
        orm_mode = True
