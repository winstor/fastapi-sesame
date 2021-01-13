from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models import SiteModel


class CRUDSite(CRUDBase[SiteModel]):
    def get_by_secret(self, db: Session, secret: Any) -> SiteModel:
        return db.query(self.model).filter(self.model.secret == secret).first()


site = CRUDSite(SiteModel)
