from typing import Optional
from pydantic import BaseModel


class ApiResponseBase(BaseModel):
    status: Optional[bool] = True
    massage: Optional[str] = None


class ApiResponse(ApiResponseBase):
    pass

    class Config:
        orm_mode = True

