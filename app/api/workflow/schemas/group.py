from pydantic import BaseModel


class GroupBase(BaseModel):
    name: str


class GroupCreate(GroupBase):
    pass


class GroupStore(GroupCreate):
    site_id: int
    creator_id: int


class GroupUpdate(GroupBase):
    pass


class Group(GroupBase):
    id: int
    site_id: int
    creator_id: int

    class Config:
        orm_mode = True
