from typing import List
from fastapi import HTTPException
from app.crud.base import CRUDBase
from sqlalchemy.orm import Session
from app.api.workflow.models import FieldModel, FieldTempModel
from app.api.workflow import models
from app.api.workflow import schemas


class CRUDField(CRUDBase):

    def filter_by(self, db: Session, **kwargs):
        return db.query(self.model).filter_by(**kwargs).order_by(self.model.order).all()

    # 发布
    def publish(self, db: Session, workflow_id: int):
        mappings = []
        field_temps = db.query(FieldTempModel).filter_by(workflow_id=workflow_id).all()
        for object in field_temps:
            mappings.append(object.to_dict())
        try:
            db.query(self.model).filter_by(workflow_id=workflow_id).delete()
            db.bulk_insert_mappings(self.model, mappings)
            # if field_ids:
            # 需要删除业务申请表中相关字段数据
            # db.query(DataModel).filter_by(workflow_id=workflow.id,field_id=delete_id).delete()
            db.commit()
        except Exception:
            db.rollback()
            raise HTTPException(status_code=404, detail="发布失败")
        return db.query(self.model).filter_by(workflow_id=workflow_id).all()


field = CRUDField(FieldModel)
