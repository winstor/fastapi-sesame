from typing import Any, Dict, Optional, Union
from sqlalchemy.orm import Session
from app.core.security import get_password_hash, verify_password
from app.crud.base import CRUDBase
from app.models import UserModel
from app.schemas.user import UserCreate, UserUpdate
import json


class CRUDUser(CRUDBase[UserModel]):

    def get_by_email(self, db: Session, *, email: str) -> Optional[UserModel]:
        return db.query(self.model).filter(self.model.email == email).first()

    def get_by_username(self, db: Session, *, site_id: int, username: str) -> Optional[UserModel]:
        return db.query(self.model).filter(
            self.model.site_id == site_id
        ).filter(
            self.model.username == username
        ).first()

    def get_by_wx_openid(self, db: Session, wx_openid: str) -> Optional[UserModel]:
        return db.query(self.model).filter(self.model.wx_openid == wx_openid).first()

    def create(self, db: Session, *, obj_in:  Union[UserCreate, Dict[str, Any]]) -> UserModel:
        if isinstance(obj_in, dict):
            create_data = obj_in
        else:
            create_data: dict = obj_in.dict(exclude_unset=True)
        create_data["hashed_password"] = get_password_hash(create_data["password"])
        del create_data["password"]
        return super().create(db=db, obj_in=create_data)

    def create_by_wechat(self, db: Session, wx_openid: str, name: str = None, avatar: str = None):
        db_user = self.model(wx_openid=wx_openid, name=name, avatar=avatar)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    def update(
            self, db: Session, *, db_obj: UserModel, obj_in: Union[UserUpdate, Dict[str, Any]]
    ) -> UserModel:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        if "password" in update_data:
            if update_data["password"]:
                update_data["hashed_password"] = get_password_hash(update_data["password"])
            del update_data["password"]
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def authenticate(self, db: Session, *, site_id: int, username: str, password: str) -> Optional[UserModel]:
        db_user = self.get_by_username(db, site_id=site_id, username=username)
        if not db_user:
            return None
        if not verify_password(password, db_user.hashed_password):
            return None
        return db_user

    # 是否根管理员
    @staticmethod
    def is_root(db_user: UserModel):
        return db_user.is_root

    @staticmethod
    def get_scopes(db_user: UserModel):
        return json.loads(db_user.scopes)

    @staticmethod
    def disabled(db_user: UserModel) -> bool:
        return db_user.disabled

    # 是否站点管理员
    @staticmethod
    def is_mgmt(db_user: UserModel):
        return db_user.is_mgmt


user = CRUDUser(UserModel)
