from typing import Optional

from pydantic import BaseModel


# Shared properties
class SiteBase(BaseModel):
    site_name: Optional[str] = None


class SiteCreate(SiteBase):
    site_name: str


class SiteUpdate(SiteBase):
    site_name: str


# Properties shared by models stored in DB
class SiteInDBBase(SiteBase):
    id: int

    class Config:
        orm_mode = True


class Site(SiteInDBBase):
    site_name: Optional[str] = None
    parent_site_id: Optional[int] = 0
    verify_code: Optional[str] = None


