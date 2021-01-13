from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.api.workflow.models import WorkflowModel, ApplyModel


class CRUDWorkflow(CRUDBase[WorkflowModel]):
    @staticmethod
    def get_applies(db: Session, workflow_id: int, **kwargs):
        kwargs.update({"workflow_id": workflow_id})
        return db.query(ApplyModel).order_by(ApplyModel.id.desc()).filter_by(**kwargs).all()


workflow = CRUDWorkflow(WorkflowModel)
