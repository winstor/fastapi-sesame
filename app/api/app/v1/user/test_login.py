from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas.token import Token
from app.core import security
from app import crud
from app.db.database import database
from app.api.app.common import user_deps as common

DB = database.connection("local")

router = APIRouter()


#   site: models.SiteModel = Depends(common.get_auth_site)

# 获取
@router.post("/login/access-token")
async def get_token(
        db: Session = Depends(DB.get_db),
        form_data: OAuth2PasswordRequestForm = Depends(),
):
    # 判断账号密码 如果错误返回 None
    db_user = crud.user.authenticate(
        db, site_id=1, username=form_data.username, password=form_data.password
    )
    if not db_user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
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
        "token": access_token,
        "token_type": "bearer"
    })
