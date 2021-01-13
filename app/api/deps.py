from typing import List, Union, Any
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
import time
from fastapi import Depends, HTTPException, status
from fastapi.responses import JSONResponse, Response
from sqlalchemy.orm import Session
from app import crud
from app.db.database import database
from app.models import UserModel
from app.core import security
from app import schemas
from fastapi.security import (
    OAuth2PasswordBearer,
    SecurityScopes,
)

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/login/access-token",
    # scopes={"me": "Read information about the current user.", "items": "Read items."},
)


def get_db(db: Session = Depends(database.get_db)):
    return db


def get_token_payload(token: str = Depends(oauth2_scheme)):
    payload = security.token_decode(token)
    return payload


def get_token_data(payload=Depends(get_token_payload)):
    token_data = schemas.TokenPayload(**payload)
    return token_data


def get_token_scopes(payload=Depends(get_token_payload)) -> list:
    scopes = payload.get("scopes", [])
    return scopes


def get_current_uid(payload=Depends(get_token_payload)):
    token_data = schemas.TokenPayload(**payload)
    return int(token_data.sub)


def get_current_sid(payload=Depends(get_token_payload)):
    token_data = schemas.TokenPayload(**payload)
    return int(token_data.site_id)


def get_current_uname(payload=Depends(get_token_payload)):
    token_data = schemas.TokenPayload(**payload)
    return str(token_data.nickname)


def validate_scopes(security_scopes: SecurityScopes, token_scopes=Depends(get_token_scopes)):
    for scope in security_scopes.scopes:
        if scope not in token_scopes:
            raise HTTPException(
                status_code=401,
                detail="Not enough permissions",
            )
    return True


def get_current_user(
        db: Session = Depends(database.get_db), token: str = Depends(oauth2_scheme)
) -> UserModel:
    payload = security.token_decode(token)
    token_data = schemas.TokenPayload(**payload)
    current_user = crud.user.get(db=db, id=token_data.sub)
    if not current_user:
        raise HTTPException(status_code=400, detail="User not found")
    if crud.user.disabled(current_user):
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def get_current_active_user(
        current_user: UserModel = Depends(get_current_user)
) -> UserModel:
    return current_user


def get_current_mgmt(
        current_user: UserModel = Depends(get_current_user)
) -> UserModel:
    if not crud.user.is_mgmt(current_user):
        raise HTTPException(status_code=401, detail="UNAUTHORIZED")
    return current_user


def get_current_root(
        current_user: UserModel = Depends(get_current_user)
) -> UserModel:
    if crud.user.disabled(current_user):
        raise HTTPException(status_code=400, detail="User not found")
    if not crud.user.is_root(current_user):
        raise HTTPException(status_code=401, detail="UNAUTHORIZED")
    return current_user


def get_user_scopes(db_user: UserModel):
    if crud.user.is_root(db_user):
        scopes = ["root"]
    elif crud.user.is_mgmt(db_user):
        scopes = ["mgmt"]
    else:
        scopes = crud.user.get_scopes(db_user)
    return scopes


def response_token(access_token: str):
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


def resp_200(*, data: Any) -> Response:
    data = jsonable_encoder(data)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            'code': 20000,
            'message': "",
            'data': data
        }
    )


def resp_400(*, data: str = None, message: str = "") -> Response:
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            'code': 400,
            'message': message,
            'data': data
        }
    )
