from fastapi import APIRouter

from .wechat.server import wechat_router

api_router = APIRouter()

api_router.include_router(wechat_router,  tags=["wechat server"])

