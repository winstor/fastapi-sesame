from fastapi import FastAPI, Depends
from app.wechat import wechat_router
from app.api.user.v1.api import api_router as user_v1_router
from .db import database
from sqlalchemy.orm import Session
from app.extensions import site_sign

database.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

# 某某高校
site_id = 1
site_secret = '1133b733353411eb94b7d8cb8a079b7c'


@app.get("/")
async def root():
    return "高校开发版本！"


# sign 获取站点登录授权签名
@app.get("/auth_sign")
async def get_sign():
    return site_sign.sign_encode(site_secret)


# 微信服务端  临时添加, 正式环境单独运行
app.include_router(wechat_router)
# api版本v1
app.include_router(user_v1_router, prefix='/api/v1')

'''
运行 命令
uvicorn app.main:app --reload

'''

# uvicorn app.root:app --reload --port=8801
