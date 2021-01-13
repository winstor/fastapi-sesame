from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.workflow import crud, schemas
from app.api.workflow import deps

router = APIRouter()


@router.get('/')
async def reads(
        *,
        db: Session = Depends(deps.get_db),
        current_site_id: int = Depends(deps.get_current_sid)
) -> Any:
    groups = crud.workflow_group.filter_by(db=db, site_id=current_site_id)
    workflows = crud.workflow.filter_by(db=db, site_id=current_site_id)
    obj_routers = {}
    for group in groups:
        obj_routers[group.id] = {
            "id": group.id,
            "name": group.name,
            "children": []
        }
    for workflow in workflows:
        obj_routers[workflow.group_id]["children"].append({
            "id": workflow.id,
            "group_id": workflow.group_id,
            "name": workflow.workflow_name
        })
    data = []
    for (k, v) in obj_routers.items():
        data.append(v)
    return deps.resp_200(data={"groups": data})
