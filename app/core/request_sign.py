import hashlib
import time
from fastapi import HTTPException
import requests
from app.config import filesystems

SALT = "df@f2"


def create_site_sign(timestamp, salt: str = None) -> str:
    if not salt:
        salt = SALT
    md5_obj = hashlib.md5()
    md5_obj.update((str(timestamp) + salt).encode(encoding="utf-8"))
    return md5_obj.hexdigest()


def check_site_sign(timestamp: int = 0, sign: str = None):
    now = int(time.time()) - 500
    if now > timestamp:
        raise HTTPException(status_code=401, detail='签名时间过期')
    original_sign = create_site_sign(timestamp)
    if sign == original_sign:
        return True
    else:
        raise HTTPException(status_code=401, detail='签名错误')


def delete_file_notification(names: list, file=None):  # 提前定义好任务
    timestamp = int(time.time())
    sign = create_site_sign(timestamp)
    base_url = filesystems.disks.get(filesystems.default).get("url").strip('/')
    if isinstance(names, list):
        name = ','.join(names)
    else:
        name = str(names)
    url = f"{base_url}/api/files/delete?timestamp={timestamp}&sign={sign}&name={name}"
    requests.post(url, files={"file": file})
