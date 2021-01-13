import asyncio
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas.token import Token
from app.core import security
from app import crud, models
from app.db.database import database
from app.core.cache import Cache
from app.models import UserModel
from app.api.app.common import user_deps as common

router = APIRouter()


#   site: models.SiteModel = Depends(common.get_auth_site)

# 获取
@router.post("/access-token", response_model=Token)
async def get_token(
        db: Session = Depends(database.get_db),
        form_data: OAuth2PasswordRequestForm = Depends(),
        current_site: models.SiteModel = Depends(common.get_current_site)
):
    if not current_site:
        raise HTTPException(status_code=400, detail="system error")
    # 判断账号密码 如果错误返回 None
    db_user = crud.user.authenticate(
        db, site_id=current_site.id, username=form_data.username, password=form_data.password
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
        "access_token": access_token,
        "token_type": "bearer"
    })


# 长连接 监听scan扫码情况是否
@router.get("/monitor_scan", response_model=Token)
async def monitor_scan(
        db: Session = Depends(database.get_db),
        *,
        scan: str
):
    if not scan:
        raise HTTPException(status_code=400, detail="Could not Found scan")
    for i in range(60):
        wx_openid = Cache.get(key=scan)
        if not wx_openid:
            await asyncio.sleep(1)

        db_user = crud.user.get_by_wx_openid(db, wx_openid)
        if not db_user:
            raise HTTPException(status_code=400, detail="scan system error")
        # 返回token
        return {"code": True}

    raise HTTPException(status_code=408, detail="request timeout")


# 长连接 监测scan扫码情况是否
@router.get("/token_scan", response_model=Token)
async def get_token_by_scan(
        db: Session = Depends(database.get_db),
        current_site=Depends(common.get_current_site),
        *,
        scan: str
):
    if not scan:
        raise HTTPException(status_code=400, detail="Could not Found")
    wx_openid = Cache.get(key=scan)
    if not wx_openid:
        raise HTTPException(status_code=400, detail="Could not Found")

    db_user = crud.user.get_by_wx_openid(db, wx_openid)
    if not db_user:
        raise HTTPException(status_code=400, detail="scan system error")

    db_site_user = crud.site_user.get_by_site_user(db=db, site_id=current_site.id, user_id=db_user.id)
    if not db_site_user:
        raise HTTPException(status_code=400, detail="Inactive user")
    elif crud.site_user.disabled(db_site_user):
        raise HTTPException(status_code=400, detail="Inactive user")
    # 获取用户作用域
    access_token = security.create_access_token(
        data={
            "sub": str(db_user.id),
            "site_id": current_site.id,
            "scopes": [],
        }
    )
    # 返回token
    return common.response_token(access_token)


# 刷新token
@router.get("/refresh", response_model=Token)
async def refresh_token(
        token_data: UserModel = Depends(common.get_token_data),
):
    access_token = security.create_access_token(token_data.dict())
    # 返回token
    return common.response_token(access_token)
