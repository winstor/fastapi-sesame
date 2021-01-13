import json
from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.workflow import crud, schemas
from app.api.workflow import deps

router = APIRouter()


# , response_model=List[schemas.Workflow]
@router.get('/{workflow_id}')
async def reads(
        *,
        db: Session = Depends(deps.get_db),
        current_site_id: int = Depends(deps.get_current_sid),
        workflow_id: int,
        skip: int = 0,
        limit: int = 100,
) -> Any:
    workflow = crud.workflow.get(db=db, id=workflow_id)
    if not workflow or workflow.site_id != current_site_id:
        return deps.resp_200(data=[])
    applies = crud.workflow.get_applies(db=db, workflow_id=workflow_id)
    return deps.resp_200(data=applies)


# , response_model=schemas.Workflow
@router.post("/{workflow_id}")
async def create(
        *,
        db: Session = Depends(deps.get_db),
        workflow_id: int,
        obj_in: schemas.ApplyCreate,
        current_site_id: int = Depends(deps.get_current_sid),
        current_uid: int = Depends(deps.get_current_uid),
        current_uname: str = Depends(deps.get_current_uname),
) -> Any:
    # 判断流程组
    workflow = crud.workflow.get(db=db, id=workflow_id)
    if not workflow or workflow.site_id != current_site_id:
        raise HTTPException(status_code=404, detail="group not found")
    field_ids = list(str(field.id) for field in crud.field.filter_by(db=db, workflow_id=workflow_id))
    obj_data_in = obj_in.dict()
    for field_id in obj_in.data:
        if field_id not in field_ids:
            del obj_data_in["data"][field_id]
    obj_data_in.update({
        "workflow_id": workflow.id,
        "creator_id": current_uid,
        "create_user": current_uname,
        "data": json.dumps(obj_data_in['data'])
    })
    apply = crud.workflow_apply.create(db=db, obj_in=obj_data_in)
    return deps.resp_200(data=apply)


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
