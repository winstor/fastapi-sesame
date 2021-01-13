from pydantic import BaseModel


class WorkflowGroupBase(BaseModel):
    name: str


class WorkflowGroupCreate(WorkflowGroupBase):
    pass


class WorkflowGroupStore(WorkflowGroupCreate):
    site_id: int
    creator_id: int


class WorkflowGroupUpdate(WorkflowGroupBase):
    pass


class WorkflowGroup(WorkflowGroupBase):
    id: int
    site_id: int
    creator_id: int

    class Config:
        orm_mode = True
