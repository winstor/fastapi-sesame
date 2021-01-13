from fastapi import APIRouter, Depends, UploadFile, Form, HTTPException
from app.db.database import database
from app.api import deps
from sqlalchemy.orm import Session
import os
import time
import uuid
from app.schemas import TokenPayload
from app import crud
from app.schemas import FileCreate
from app.api.app.common import file_deps as common

router = APIRouter()


@router.post("/post")
async def put_file(
        db: Session = Depends(database.get_db),
        file: UploadFile = Depends(common.get_filter_file),
        # token_data: TokenPayload = Depends(deps.get_token_data)
        token: str = Form(...)
):
    token_payload = deps.get_token_payload(token)
    token_data = deps.get_token_data(token_payload)
    path_date = time.strftime("%Y%m", time.localtime())
    base_path = f"images/{token_data.site_id}/{path_date}/"
    if not os.path.exists(base_path):
        os.makedirs(base_path)
    path = base_path + uuid.uuid1().hex
    try:
        res = await file.read()
        with open(path, "wb") as f:
            f.write(res)
            f.close()
        # obj_in = FileCreate(**{
        #     'site_id': token_data.site_id,
        #     'user_id': token_data.sub,
        #     'path': path
        # })
        # crud.file.create()
    except Exception:
        raise HTTPException(status_code=404, detail="上传失败")
    return deps.resp_200(data=[{"token": token_data}])


@router.get('/test')
async def test_file():
    print(9999999999999999999)
    return {"tt": 2}


@router.put('/replace')
async def replace_file():
    return '替换'
