import json
from fastapi import APIRouter
from wechatpy import WeChatClient
from app.config import wechat
from pydantic import BaseModel

router = APIRouter()


class Qrcode(BaseModel):
    url: str
    expire_at: int


# 获取微信公众号临时二维码 用于登录、注册
@router.get("/qrcode", response_model=Qrcode)
async def get_wechat_qrcode():
    client = WeChatClient(wechat.app_id, wechat.secret)
    expire_seconds = 1800
    res = client.qrcode.create({
        # 有效时间秒
        'expire_seconds': expire_seconds,
        'action_name': 'QR_LIMIT_STR_SCENE',
        'action_info': {
            'scene': {'scene_str': "register_or_login"},
        }
    })
    #  数值需测试
    res = json.loads(res)
    url = client.qrcode.get_url(res['ticket'])
    return {"url": url, "expire_at": expire_seconds}
