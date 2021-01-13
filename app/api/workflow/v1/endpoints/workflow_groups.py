from typing import Any, List
from fastapi import APIRouter, Depends, Security, HTTPException
from sqlalchemy.orm import Session
from app.api.workflow import crud, models, schemas
from app.api.workflow import deps

router = APIRouter()


# , response_model=List[schemas.Group]
@router.get('/')
async def read_groups(
        *,
        db: Session = Depends(deps.get_db),
        current_site_id: int = Depends(deps.get_current_sid),
        skip: int = 0,
        limit: int = 100,
) -> Any:
    groups = crud.workflow_group.get_multi_by(db=db, site_id=current_site_id, skip=skip, limit=limit)
    return deps.resp_200(data=groups)


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
    group = crud.workflow_group.create(db=db, obj_in=group_in)
    return deps.resp_200(data=group)


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
    group = crud.workflow_group.get(db=db, id=id)
    if not group or group.site_id != current_site_id:
        raise HTTPException(status_code=404, detail="not found")
    group = crud.workflow_group.update(db=db, db_obj=group, obj_in=obj_in)
    return deps.resp_200(data=group)


# , response_model=schemas.Group
@router.get("/{id}")
async def read_group(
        *,
        db: Session = Depends(deps.get_db),
        id: int,
        current_site_id: int = Depends(deps.get_current_sid),
) -> Any:
    group = crud.workflow_group.get(db=db, id=id)
    if not group or group.site_id != current_site_id:
        raise HTTPException(status_code=404, detail="not found")
    return deps.resp_200(data=group)


@router.delete("/{id}", response_model=schemas.Group)
async def delete_group(
        *,
        db: Session = Depends(deps.get_db),
        id: int,
        current_site_id: int = Depends(deps.get_current_sid),
) -> Any:
    group = crud.workflow_group.get(db=db, id=id)
    if not group or group.site_id != current_site_id:
        raise HTTPException(status_code=404, detail="not found")
    crud.workflow_group.remove(db=db, id=id)
    return deps.resp_200(data=group)
