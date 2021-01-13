import json
from typing import Any, Optional, List, Union
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, validator


class UserBase(BaseModel):
    user_id: int
    user_name: str


class FieldBase(BaseModel):
    id: int
    state: int


class EdgeBase(BaseModel):
    source: Union[str, int]
    target: Union[str, int]


class ExtendData(BaseModel):
    x: int
    y: int


class NodeTempCreate(BaseModel):
    id: int
    node_name: str
    node_type: str
    source: Optional[List[str]] = []
    target: str
    field: Optional[List[FieldBase]] = None
    user: Optional[List[int]] = None
    extend_data: ExtendData

    @validator('source')
    def dumps_source(cls, source: Optional[List[str]] = []):
        return json.dumps(source)

    @validator('field')
    def dumps_field(cls, field: List[FieldBase]):
        return json.dumps(jsonable_encoder(field))

    @validator('user')
    def dumps_user(cls, user: List[int]):
        return json.dumps(user)

    @validator('extend_data')
    def dumps_extend_data(cls, extend_data: Optional[ExtendData]=None):
        return json.dumps(extend_data.dict())


class NodeTemp(BaseModel):
    id: int

    # @validator('options')
    # def create_time_format(cls, options: str):
    #     return json.loads(options)

    class Config:
        orm_mode = True
