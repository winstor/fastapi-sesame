from typing import Any, List
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.api.workflow import schemas
from app.crud.base import CRUDBase
from app.api.workflow.models import FieldTempModel, FieldModel
from app.api.workflow import models


class CRUDFieldTemp(CRUDBase):

    def filter_by(self, db: Session, **kwargs):
        return db.query(self.model).filter_by(**kwargs).order_by(self.model.order).all()

    def multi_save_all(
            self,
            db: Session,
            workflow: models.WorkflowModel,
            obj_lists: List[schemas.FieldCreate]
    ):
        field_ids = list(db_filed.id for db_filed in db.query(self.model).filter_by(workflow_id=workflow.id).all())
        insert_objects = []
        update_mappings = []
        for order, obj_in in enumerate(obj_lists):
            obj_data_in: dict = obj_in.dict()
            obj_data_in.update({"workflow_id": workflow.id, "order": order})
            if obj_in.id in field_ids:
                field_ids.remove(obj_in.id)
                update_mappings.append(obj_data_in)
            else:
                obj_data_in.pop("id")
                insert_objects.append(obj_data_in)
        try:
            # 批量删除
            if insert_objects:
                db.bulk_insert_mappings(self.model, insert_objects)
            if update_mappings:
                db.bulk_update_mappings(self.model, update_mappings)
            if field_ids:
                [db.query(self.model).filter_by(id=id).delete() for id in field_ids]
            # db.query(self.model).filter_by(workflow_id=workflow.id).delete()
            # 批量导入
            # db.bulk_insert_mappings(self.model, insert_objects)
            db.commit()
        except Exception:
            db.rollback()
            raise HTTPException(status_code=404, detail="保存失败")
        return db.query(self.model).filter_by(workflow_id=workflow.id).order_by(self.model.order).all()


field_temp = CRUDFieldTemp(FieldTempModel)
