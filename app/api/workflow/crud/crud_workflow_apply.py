from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.api.workflow.models import ApplyModel, NodeUserModel


class CRUDWorkflowApply(CRUDBase[ApplyModel]):
    def search_apply(self, db: Session, site_id: int, user_id: int, *, skip: int = 0, limit: int = 100):
        workflow_ids = db.query(self.model).join(NodeUserModel, ApplyModel.workflow_id == NodeUserModel.workflow_id)


workflow_apply = CRUDWorkflowApply(ApplyModel)
