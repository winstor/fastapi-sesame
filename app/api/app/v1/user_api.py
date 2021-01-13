from fastapi import APIRouter

from .user import wechat, users, login, owns

api_router = APIRouter()


# api_router.include_router(login.router,  tags=["login"])
# 个人信息
api_router.include_router(owns.router, prefix="/user",  tags=["user"])

api_router.include_router(users.router, prefix="/users", tags=["users"])

# api_router.include_router(wechat.router, prefix="/wechat", tags=["wechat"])