from typing import Optional, List
from fastapi import Depends, APIRouter, Depends, HTTPException
from app.db.database import database
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.api.app.common import user_deps as common
from app.models import UserModel
from app import models
from app import crud, schemas

router = APIRouter()


class User(BaseModel):
    id: int
    username: Optional[str] = None
    name: Optional[str] = None
    mobile: Optional[str] = None
    email: Optional[str] = None
    disabled: Optional[bool] = None


@router.get("/")
async def read_users(
        db: Session = Depends(database.get_db),
        current_user: models.SiteUserModel = Depends(common.get_current_mgmt),
        skip: int = 0,
        limit: int = 100
):
    users = crud.user.get_multi(db=db, skip=skip, limit=limit)
    return users


@router.get("/all")
async def read_users(
        db: Session = Depends(database.get_db),
        current_user: models.SiteUserModel = Depends(common.get_current_mgmt),
):
    users = crud.user.filter_by(db=db, site_id=current_user.site_id)
    data = []
    for user in users:
        user = user.to_dict()
        data.append(schemas.UserOut(**user))
    return common.resp_200(data=data)


@router.put("/disable/{user_id}")
async def read_users(
        db: Session = Depends(database.get_db),
        current_user: models.SiteUserModel = Depends(common.get_current_mgmt),
        *
        user_id: int
):
    user: UserModel = crud.user.get(db=db, id=user_id)
    if not user:
        raise HTTPException(status_code=401, detail="not fond")
    if user.site_id == current_user.site_id:
        crud.user.remove(db=db, id=user_id)
        return {}
    else:
        raise HTTPException(status_code=401, detail="not fond")
