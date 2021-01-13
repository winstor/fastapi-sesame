from typing import Any, List, Optional
from pydantic import BaseModel
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.workflow import crud, schemas
from app.api.workflow import deps

router = APIRouter()


@router.get('/', response_model=List[schemas.FieldCate])
async def index(
        db: Session = Depends(deps.get_db),
) -> Any:
    field_cate = crud.field_cate.all(db=db)
    return deps.resp_200(data=field_cate)


@router.post("/", response_model=schemas.FieldCate)
async def create(
        *,
        db: Session = Depends(deps.get_db),
        obj_in: schemas.FieldCateCreate,
) -> Any:
    object = crud.field_cate.create(db=db, obj_in=obj_in)
    return object


@router.put("/{id}", response_model=schemas.FieldCate)
async def update(
        *,
        db: Session = Depends(deps.get_db),
        id: int,
        obj_in: schemas.FieldCateUpdate,
) -> Any:
    cate = crud.field_cate.get(db=db, id=id)
    if not cate:
        raise HTTPException(status_code=404, detail="not found")
    cate = crud.field_cate.update(db=db, db_obj=cate, obj_in=obj_in)
    return cate


@router.get("/{id}", response_model=schemas.FieldCate)
async def show(
        *,
        db: Session = Depends(deps.get_db),
        id: int,
) -> Any:
    field_cate = crud.field_cate.get(db=db, id=id)
    return field_cate


@router.delete("/{id}", response_model=schemas.FieldCate)
async def delete(
        *,
        db: Session = Depends(deps.get_db),
        id: int,
) -> Any:
    cate = crud.field_cate.remove(db=db, id=id)
    return cate
