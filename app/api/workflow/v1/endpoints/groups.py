from typing import Any, List
from fastapi import APIRouter, Depends, Security, HTTPException
from sqlalchemy.orm import Session
from app.api.workflow import crud, models, schemas
from app.api.workflow import deps
from app.crud.base import CRUDBase

group = CRUDBase(models.GroupModel)


router = APIRouter()


@router.get('/', response_model=List[schemas.Group])
async def read_groups(
        *,
        db: Session = Depends(deps.get_db),
        current_site_id: int = Depends(deps.get_current_sid),
        skip: int = 0,
        limit: int = 100,
) -> Any:
    groups = crud.group.get_multi_by(db=db, site_id=current_site_id, skip=skip, limit=limit)
    return groups


@router.post("/", response_model=schemas.Group)
async def create_group(
        *,
        db: Session = Depends(deps.get_db),
        group_in: schemas.GroupCreate,
        current_site_id: int = Depends(deps.get_current_sid),
        current_uid: int = Depends(deps.get_current_uid),
) -> Any:
    obj_in = group_in.dict()
    obj_in.update({"site_id": current_site_id, "creator_id": current_uid})
    group_in = schemas.GroupStore(**obj_in)
    group = crud.group.create(db=db, obj_in=group_in)
    return group


@router.put("/{id}", response_model=schemas.Group)
async def update_group(
        *,
        db: Session = Depends(deps.get_db),
        current_site_id: int = Depends(deps.get_current_sid),
        id: int,
        obj_in: schemas.GroupUpdate,
) -> Any:
    """
    Update an item.
    """
    group = crud.group.get(db=db, id=id)
    if not group or group.site_id != current_site_id:
        raise HTTPException(status_code=404, detail="not found")
    group = crud.group.update(db=db, db_obj=group, obj_in=obj_in)
    return group


@router.get("/{id}", response_model=schemas.Group)
async def read_group(
        *,
        db: Session = Depends(deps.get_db),
        id: int,
        current_site_id: int = Depends(deps.get_current_sid),
) -> Any:
    group = crud.group.get(db=db, id=id)
    if not group or group.site_id != current_site_id:
        raise HTTPException(status_code=404, detail="not found")
    return group


@router.delete("/{id}", response_model=schemas.Group)
async def delete_group(
        *,
        db: Session = Depends(deps.get_db),
        id: int,
        current_site_id: int = Depends(deps.get_current_sid),
) -> Any:
    group = crud.group.get(db=db, id=id)
    if not group or group.site_id != current_site_id:
        raise HTTPException(status_code=404, detail="not found")
    crud.group.remove(db=db, id=id)
    return group
