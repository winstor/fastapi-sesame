from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.workflow import crud, schemas
from app.api.workflow import deps

router = APIRouter()


# , response_model=List[schemas.Workflow]
@router.get('/')
async def reads(
        *,
        db: Session = Depends(deps.get_db),
        current_site_id: int = Depends(deps.get_current_sid),
        skip: int = 0,
        limit: int = 100,
) -> Any:
    workflows = crud.workflow.get_multi_by(db=db, site_id=current_site_id, skip=skip, limit=limit)
    return deps.resp_200(data=workflows)


# , response_model=schemas.Workflow
@router.post("/")
async def create(
        *,
        db: Session = Depends(deps.get_db),
        obj_in: schemas.WorkflowCreate,
        current_site_id: int = Depends(deps.get_current_sid),
        current_uid: int = Depends(deps.get_current_uid),
) -> Any:
    # 判断流程组
    group = crud.workflow_group.get(db=db, id=obj_in.group_id)
    if not group or group.site_id != current_site_id:
        raise HTTPException(status_code=404, detail="group not found")

    obj_in = obj_in.dict()
    obj_in.update({"site_id": current_site_id, "creator_id": current_uid})
    # obj_in = schemas.WorkflowStore(**obj_in)
    workflow = crud.workflow.create(db=db, obj_in=obj_in)
    return deps.resp_200(data=workflow)


# , response_model=schemas.Workflow
@router.put("/{workflow_id}")
async def update(
        *,
        db: Session = Depends(deps.get_db),
        current_site_id: int = Depends(deps.get_current_sid),
        workflow_id: int,
        obj_in: schemas.WorkflowUpdate,
) -> Any:
    workflow = crud.workflow.get(db=db, id=workflow_id)
    if not workflow or workflow.site_id != current_site_id:
        raise HTTPException(status_code=404, detail="not found")
    workflow = crud.workflow.update(db=db, db_obj=workflow, obj_in=obj_in)
    return deps.resp_200(data=workflow)


# , response_model=schemas.Workflow
@router.get("/{workflow_id}")
async def show(
        *,
        db: Session = Depends(deps.get_db),
        workflow_id: int,
        current_site_id: int = Depends(deps.get_current_sid),
) -> Any:
    workflow = crud.workflow.get(db=db, id=workflow_id)
    if not workflow or workflow.site_id != current_site_id:
        raise HTTPException(status_code=404, detail="not found")
    return deps.resp_200(data=workflow)


# , response_model=schemas.Workflow
@router.delete("/{workflow_id}")
async def delete(
        *,
        db: Session = Depends(deps.get_db),
        workflow_id: int,
        current_site_id: int = Depends(deps.get_current_sid),
) -> Any:
    workflow = crud.workflow.get(db=db, id=workflow_id)
    if not workflow or workflow.site_id != current_site_id:
        raise HTTPException(status_code=404, detail="not found")
    crud.workflow.remove(db=db, id=workflow_id)
    return workflow


@router.get("/field/{workflow_id}", response_model=List[schemas.Field])
async def show(
        *,
        db: Session = Depends(deps.get_db),
        current_site_id: int = Depends(deps.get_current_sid),
        workflow_id: int,
):
    workflow = crud.workflow.get(db=db, id=workflow_id)
    if not workflow or workflow.site_id != current_site_id:
        raise HTTPException(status_code=404, detail="not found")
    fields = crud.field.filter_by(db=db, workflow_id=workflow_id)
    return deps.resp_200(data=fields)


@router.get('/apply/{workflow_id}')
async def reads(
        *,
        db: Session = Depends(deps.get_db),
        current_site_id: int = Depends(deps.get_current_sid),
        workflow_id: int,
        skip: int = 0,
        limit: int = 100,
) -> Any:
    return deps.resp_200(data=[])
