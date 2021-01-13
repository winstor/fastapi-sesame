from typing import List
from app.crud.base import CRUDBase
from sqlalchemy.orm import Session
from app.api.workflow.models import WorkflowGroupModel


class CRUDWorkflowGroup(CRUDBase):
    def get_multi_by(
            self, db: Session, site_id: int, *, skip: int = 0, limit: int = 100
    ) -> List[WorkflowGroupModel]:
        return db.query(self.model).filter(self.model.site_id == site_id).offset(
            skip).limit(limit).all()


workflow_group = CRUDWorkflowGroup(WorkflowGroupModel)
