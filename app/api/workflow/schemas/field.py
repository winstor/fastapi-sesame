from typing import Any, Optional, List
from pydantic import BaseModel, validator
import json


class FieldBase(BaseModel):
    id: Optional[int] = None
    field_name: Optional[str] = None
    default: Optional[str] = None
    relation_wid: int = 0
    relation_fid: int = 0


class FieldCreate(FieldBase):
    field_name: str
    slug: str
    options: Optional[str] = '',

    # @validator('options')
    # def create_time_format(cls, options: Any):
    #     return json.dumps(options)


class Field(FieldBase):
    id: int
    workflow_id: int
    slug: str
    options: Optional[str] = None

    # @validator('options')
    # def create_time_format(cls, options: str):
    #     return json.loads(options)

    class Config:
        orm_mode = True
