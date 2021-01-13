from typing import Optional
from pydantic import BaseModel, validator
from datetime import datetime


class WorkflowBase(BaseModel):
    workflow_name: Optional[str] = None


class WorkflowCreate(WorkflowBase):
    group_id: int
    workflow_name: str


class WorkflowStore(WorkflowCreate):
    site_id: int
    creator_id: int


class WorkflowUpdate(WorkflowBase):
    pass


class Workflow(BaseModel):
    id: int
    site_id: Optional[int] = None
    group_id: Optional[int] = None
    workflow_name: Optional[str] = None
    creator_id: Optional[int] = None
    created_at: Optional[datetime] = None

    @validator('created_at')
    def create_time_format(cls, created_at: datetime):
        return created_at.strftime("%Y-%m-%d %H:%M:%S")

    class Config:
        orm_mode = True
