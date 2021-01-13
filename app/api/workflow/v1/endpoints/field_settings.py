from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.workflow import crud, schemas
from app.api.workflow import deps

router = APIRouter()


# 获取流程 字段 , response_model=List[schemas.Field]
@router.get('/{workflow_id}')
async def index(
        *,
        db: Session = Depends(deps.get_db),
        current_site_id: int = Depends(deps.get_current_sid),
        workflow_id: int,
) -> Any:
    workflow = crud.workflow.get(db=db, id=workflow_id)
    if not workflow or workflow.site_id != current_site_id:
        raise HTTPException(status_code=404, detail="not found")
    fields = crud.field_temp.filter_by(db=db, workflow_id=workflow_id)
    return deps.resp_200(data=fields)


# 保存 , response_model=List[schemas.Field]
@router.post("/{workflow_id}")
async def save_fields(
        *,
        db: Session = Depends(deps.get_db),
        obj_lists: List[schemas.FieldCreate],
        current_site_id: int = Depends(deps.get_current_sid),
        workflow_id: int,
) -> Any:
    workflow = crud.workflow.get(db=db, id=workflow_id)
    if not workflow or workflow.site_id != current_site_id:
        raise HTTPException(status_code=404, detail="not found")
    lists = crud.field_temp.multi_save_all(db=db, workflow=workflow, obj_lists=obj_lists)
    return deps.resp_200(data=lists)


# 发布
@router.put("/publish/{workflow_id}")
async def publish(db: Session = Depends(deps.get_db), *, workflow_id: int):
    crud.field.publish(db=db, workflow_id=workflow_id)
    return deps.resp_200(data='')
