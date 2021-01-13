from fastapi import APIRouter, responses, Depends, Request
from wechatpy import parse_message
from wechatpy.crypto import WeChatCrypto
from wechatpy.exceptions import InvalidSignatureException, InvalidAppIdException
from app.core.cache import cache
from app.db.database import database
from app.config import wechat
from wechatpy import WeChatClient
from sqlalchemy.orm import Session
import random
from app import crud


def dict_data(crypto_xml):
    message = parse_message(crypto_xml)
    return message.__dict__['_data']


def type_event(db: Session, message):
    if "Ticket" in message:
        client = WeChatClient(wechat.app_id, wechat.secret)
        user = crud.user.get_by_wx_openid(db, message['FromUserName'])
        # 不存在时创建用户
        if not user:
            try:
                # 获取微信
                wechat_user = client.user.get(message['FromUserName'])
            except Exception as e:
                print(e)
                nickname = "nickname" + str(random.randint(100, 999))
                headimgurl = "https://ss3.bdstatic.com/70cFv8Sh_Q1YnxGkpoWK1HF6hhy/it/u=1517507934,1319873565&fm=26&gp=0.jpg"
                wechat_user = {"openid": message['FromUserName'], "nickname": nickname, "headimgurl": headimgurl}
                # raise e
            crud.user.create_by_wechat(
                db=db,
                wx_openid=message['FromUserName'],
                name=wechat_user["nickname"],
                avatar=wechat_user["headimgurl"]
            )
        cache.set_db(db).put(key=message['Ticket'], value=message['FromUserName'], minute=5)
    return ''


def type_text():
    return ''


wechat_router = APIRouter()


# 微信服务端  接收返回消息
# 参考网址 https://github.com/jess-weigou/FastAPI-WeWork-Robot/blob/master/main.py
@wechat_router.post("/wechat/server")
async def wechat_server(
        request: Request,
        msg_signature: str,
        timestamp: int,
        nonce: int,
        db: Session = Depends(database.get_session)
):
    xml = await request.body()
    crypto = WeChatCrypto(wechat.token, wechat.encoding_aes_key, wechat.app_id)
    try:
        crypto_xml = crypto.decrypt_message(
            xml,
            msg_signature,
            timestamp,
            nonce
        )
        data = parse_message(crypto_xml)
        message = data.__dict__['_data']
        if message["MsgType"] == 'event':
            res = type_event(db, message)
        elif message["MsgType"] == 'text':
            res = type_text()
        else:
            res = ''
        return responses.HTMLResponse(res)
    except (InvalidAppIdException, InvalidSignatureException):
        # 处理异常或忽略
        pass
    return responses.HTMLResponse("")
