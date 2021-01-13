from fastapi import APIRouter, Depends
from .roots import users, login, sites
from app.api.app.common import root_deps as common

api_router = APIRouter()

# endpoints 登录
api_router.include_router(
    login.router,
    tags=["登录管理"],
)
# 用户
api_router.include_router(
    users.router,
    prefix="/users",
    tags=["用户管理"],
    dependencies=[Depends(common.get_current_root)]
)

# 站点
api_router.include_router(
    sites.router,
    prefix="/sites",
    tags=["站点管理"],
    dependencies=[Depends(common.get_current_root)]
)
