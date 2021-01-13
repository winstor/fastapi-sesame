from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from app.schemas.token import Token
from app.core import security
from app import crud, models, schemas
from app.db.database import database
from app.api.app.common import user_deps as common
from pydantic import BaseModel

router = APIRouter()


#   site: models.SiteModel = Depends(common.get_auth_site)

class UserLogin(BaseModel):
    username: str
    password: str


@router.post("/login", response_model=Token)
async def get_token(
        *,
        db: Session = Depends(database.get_db),
        form_data: UserLogin,
        current_site: models.SiteModel = Depends(common.get_current_site)
):
    if not current_site:
        raise HTTPException(status_code=400, detail="system error")
    # 判断账号密码 如果错误返回 None
    db_user = crud.user.authenticate(
        db, site_id=current_site.id, username=form_data.username, password=form_data.password
    )
    if not db_user:
        raise HTTPException(status_code=400, detail="账号或密码不正确")
    # 获取用户作用域
    scopes = ['user']
    if crud.user.is_mgmt(db_user):
        scopes = ['mgmt']
    if crud.user.is_root(db_user):
        scopes = ['root']

    access_token = security.create_access_token(
        data={
            "sub": str(db_user.id),
            "site_id": db_user.site_id,
            "nickname": db_user.name,
            "scopes": scopes,
        }
    )
    # 返回token
    return common.resp_200(data={
        "access_token": access_token,
        "token_type": "bearer"
    })


@router.get("/info")
async def user_info(
        current_user: models.UserModel = Depends(common.get_current_user),
):
    obj_in = jsonable_encoder(current_user)
    user = schemas.UserOut(**obj_in).dict()
    user['roles'] = ['test']
    # user["routers"] = [{
    #     "path": '',
    #     "component": 'Layout',
    #     "children": [{
    #         "path": 'dashboard1',
    #         "name": 'Dashboard1',
    #         "component": 'dashboard',
    #         "meta": {
    #             "title": '接口返回',
    #             "icon": 'dashboard'
    #         }
    #     }
    #     ]}
    # ]
    return common.resp_200(data=user)


@router.post("/logout")
async def user_logout(
        current_user: models.SiteUserModel = Depends(common.get_current_mgmt),
):
    return common.resp_200(data="success")
