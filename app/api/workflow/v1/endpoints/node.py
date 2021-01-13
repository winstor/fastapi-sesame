from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.workflow import crud, schemas
from app.api.workflow import deps

router = APIRouter()


@router.get('/{workflow_id}')
async def read_node_temps(
        *,
        db: Session = Depends(deps.get_db),
        current_site_id: int = Depends(deps.get_current_sid),
        workflow_id: int,
) -> Any:
    workflows = crud.workflow.get(db=db, id=workflow_id)
    if not workflows or current_site_id != workflows.site_id:
        return deps.resp_200(data=[])
    node_temps = crud.node.get_temp_all(db=db, workflow_id=workflow_id)
    return deps.resp_200(data=node_temps)


# , response_model=List[schemas.NodeTempCreate]
@router.post("/{workflow_id}")
async def create_node_temps(
        *,
        db: Session = Depends(deps.get_db),
        obj_lists: List[schemas.NodeTempCreate],
        current_site_id: int = Depends(deps.get_current_sid),
        workflow_id: int,
) -> Any:
    # 判断流程组
    workflow = crud.workflow.get(db=db, id=workflow_id)
    if not workflow or workflow.site_id != current_site_id:
        raise HTTPException(status_code=404, detail="workflow not found")
    node_temps = crud.node.multi_save_all(db=db, workflow_id=workflow_id, obj_lists=obj_lists)
    return deps.resp_200(data=node_temps)


@router.put("/publish/{workflow_id}")
async def update(
        *,
        db: Session = Depends(deps.get_db),
        current_site_id: int = Depends(deps.get_current_sid),
        workflow_id: int,
) -> Any:
    workflows = crud.workflow.get(db=db, id=workflow_id)
    if not workflows or current_site_id != workflows.site_id:
        return deps.resp_200(data=[])
    node_temps = crud.node.publish(db=db, workflow=workflows)
    return deps.resp_200(data='')


@router.get("/{workflow_id}", response_model=List[schemas.Field])
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
    return fields
