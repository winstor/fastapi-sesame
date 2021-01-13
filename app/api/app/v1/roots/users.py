from typing import Optional, List, Any
from fastapi import Depends, APIRouter, Depends, HTTPException, Body
from app.db.database import database
from sqlalchemy.orm import Session
from app.api.app.common import root_deps as common
from app.models import UserModel
from app import crud
from app import schemas

router = APIRouter()


# from app.api.middleware.check_token import CheckTokenHandler
# router.route_class = CheckTokenHandler


class UserOut(schemas.UserOut):
    is_root: bool


@router.get("/", response_model=List[UserOut])
async def read_users(
        db: Session = Depends(database.get_db),
        skip: int = 0,
        limit: int = 100
):
    users = crud.user.get_multi(db=db, skip=skip, limit=limit)
    return users


@router.get("/{id}", response_model=UserOut)
async def read_user(
        *,
        db: Session = Depends(database.get_db),
        id: int
):
    users = crud.user.get(db=db, id=id)
    return users


@router.post("/")
async def create_user(
        *,
        db: Session = Depends(database.get_db),
        obj_in: schemas.UserCreate
):
    user = crud.user.create(db, obj_in=obj_in)
    return user


# obj_in: UserSchema,
@router.put("/{id}")
async def update_user(
        *,
        db: Session = Depends(database.get_db),
        id: int,
        obj_in: schemas.UserUpdate,
):
    user: UserModel = crud.user.get(db=db, id=id)
    if not user:
        raise HTTPException(status_code=400, detail='not found')
    user = crud.user.update(db, db_obj=user, obj_in=obj_in)
    return user
