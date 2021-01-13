from datetime import datetime, timedelta
from typing import List, Optional

from fastapi import Depends, FastAPI, HTTPException, Security, status, File, UploadFile
from fastapi.security import (
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm,
    SecurityScopes,
)
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel, ValidationError
import uuid
import requests

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Chains",
        "email": "alicechains@example.com",
        "hashed_password": "$2b$12$gSvqqUPvlXP2tfVFaWK1Be7DlH.PKZbv5H8KnzzVgXXbVxpva.pFm",
        "disabled": True,
    },
}


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None
    scopes: List[str] = []


class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None


class UserInDB(User):
    hashed_password: str


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

#  tokenUrl scopes  参数添加 docs 使用
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="token",
    scopes={"me": "Read information about the current user.", "items": "Read items."},
)

app = FastAPI()


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(
        security_scopes: SecurityScopes, token: str = Depends(oauth2_scheme)
):
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = f"Bearer"
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": authenticate_value},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(payload)
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_scopes = payload.get("scopes", [])
        token_data = TokenData(scopes=token_scopes, username=username)
    except (JWTError, ValidationError):
        raise credentials_exception
    user = get_user(fake_users_db, username=token_data.username)
    print(security_scopes.scopes)
    print(token_data.scopes)
    if user is None:
        raise credentials_exception
    for scope in security_scopes.scopes:
        if scope not in token_data.scopes:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not enough permissions",
                headers={"WWW-Authenticate": authenticate_value},
            )
    return user


async def get_current_active_user(
        current_user: User = Security(get_current_user, scopes=["me"])
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "test": "1234a", "scopes": form_data.scopes},
        expires_delta=access_token_expires,
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


@app.get("/users/me/items/")
async def read_own_items(
        current_user: User = Security(get_current_active_user, scopes=["items"])
):
    return [{"item_id": "Foo", "owner": current_user.username}]


@app.post("/status/")
async def read_system_status():
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36",
        "cookie": "XSRF-TOKEN=eyJpdiI6ImlIb3VHMmc0UFV1VHdNVnIyc01UcGc9PSIsInZhbHVlIjoiUE9XTkNBVmgyZ3pLTHZqalpWK1JpcGJTMmlSR1djMHAybkZjYjZVVFBPdHA3VWhlaHFCMXZVelVlQldkZkRzbzh0c1A1YXlwYmdRc2I5S2YrZWd2TXFUcUVCbVdEZjdYNzVzTlNuT3F2NXB4b2thUU81Y2dnSHo4WG1oTmVaQmEiLCJtYWMiOiI1MDE1MWI5OGUxMTgwNTBhMmE2MmMxNjUxOWZhNWM5MTM2MjdlYTdlNDlmNGViNjBmN2Q2NzVmODY3ODcxZjVjIn0%3D; wookteam_session=eyJpdiI6InNBbmkrZ2EwRm1GZDZIalJDOHdLNEE9PSIsInZhbHVlIjoiYWdicXM2cEZOSkk4c0hkb09HeGN1Y0V1aEtTemkvN2J3SEwra1pGNTZNWldjTkRXaEJ2RlM1OFM0dkE2V1J3Nm9peDd1K0FROU5IR0dISGJKTFBrZlV1ZnRvNml5NHd4R1Z5d01wYW1vTXpaZEh6Q3hIT0d4b09hb0x2SFp6L0UiLCJtYWMiOiIwOTBkNDg2MWEyYzQ0YjM2MDgzOGIzNjJjNWU2ZGE2MmUwYjE2ZjBlZTA4NGZhMGY1MDU3NzI4OWFmNDk0NzMxIn0%3D"
    }
    path = "app\\1.png"
    files = {'files': open(path, 'rb')}
    data = {
        "token": "MjI1QGppbmdsaUBIemFIbmdAMTYwNjQ2MDA1MUBrOFRhRjE=",
        "taskid": "1777",
        "projectid": 536,
        "files": open(path, 'rb')
    }
    url = "https://demo.wookteam.com/api/project/files/upload"
    try:
        upload_res = requests.post(url=url, data=data, files=files, headers=header)
        print(upload_res.content)
    except Exception as e:
        print(e)
    return 22
    uuid4_9 = uuid.uuid4()
    return {
        "uuid1_1": uuid.uuid1(),
        "uuid1_2": uuid.uuid1(),
        "uuid1_3": uuid.uuid1(),
        "uuid1_4": uuid.uuid1(),
        "uuid4_1": uuid.uuid4(),
        "uuid4_2": uuid.uuid4(),
        "uuid4_3": uuid.uuid4(),
        "uuid4_4": uuid.uuid4(),
        "uuid4_5": uuid.uuid4(),
        "uuid4_6": uuid.uuid4(),
        "uuid4_7": uuid.uuid4(),
        "uuid4_8": uuid.uuid4().hex,
        "uuid4_9_1": uuid4_9,
        "uuid4_9_2": uuid4_9.hex,
    }
