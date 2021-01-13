from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from app.core.jwt import oauth
from app.api.deps import Session, database
from app.api.sesame import crud
from app.api.sesame.models import UserModel

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def get_current_user(payload: dict = Depends(oauth.decode)) -> UserModel:
    user_id: str = payload.get("sub")


def get_current_user(
        db: Session = Depends(database.get_db), payload: dict = Depends(oauth.decode)
) -> UserModel:
    current_user = crud.user.get(db=db, id=payload.get("sub"))
    if not current_user:
        raise HTTPException(status_code=400, detail="User not found")
    if crud.user.disabled(current_user):
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
