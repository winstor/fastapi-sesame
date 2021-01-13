from typing import Optional

from pydantic import BaseModel


# Shared properties
class SiteUserBase(BaseModel):
    pass


class SiteUserCreate(SiteUserBase):
    site_id: int
    user_id: int
    is_mgmt: Optional[bool] = False



class SiteUserUpdate(SiteUserBase):
    pass


# Properties shared by models stored in DB
class SiteUserInDBBase(SiteUserBase):
    id: int

    class Config:
        orm_mode = True


class SiteUser(SiteUserInDBBase):
    pass
