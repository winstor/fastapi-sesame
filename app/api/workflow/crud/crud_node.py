import json
from typing import Any, List
from fastapi.encoders import jsonable_encoder
from fastapi import HTTPException
from app.crud.base import CRUDBase
from sqlalchemy.orm import Session
from app.api.workflow.models import NodeModel, NodeTempModel, NodeUserModel, NodeLinkModel
from app.api.workflow import crud, schemas, models


class CRUDNode(CRUDBase):
    @staticmethod
    def get_temp_all(db: Session, workflow_id: int):
        return db.query(NodeTempModel).filter_by(workflow_id=workflow_id).all()

    @staticmethod
    def multi_save_all(db: Session, workflow_id: int, obj_lists: List[schemas.NodeTempCreate]):
        node_ids = list(node_temp.id for node_temp in db.query(NodeTempModel).filter_by(workflow_id=workflow_id).all())
        insert_objects = []
        update_mappings = []
        for obj_in in obj_lists:
            obj_data_in = obj_in.dict()
            obj_data_in.update({"workflow_id": workflow_id})
            if obj_in.id in node_ids:
                node_ids.remove(obj_in.id)
                update_mappings.append(obj_data_in)
            else:
                obj_data_in.pop("id")
                insert_objects.append(obj_data_in)
        try:
            # 批量删除
            if insert_objects:
                db.bulk_insert_mappings(NodeTempModel, insert_objects)
            if update_mappings:
                db.bulk_update_mappings(NodeTempModel, update_mappings)
            if node_ids:
                [db.query(NodeTempModel).filter_by(id=id).delete() for id in node_ids]
            # 批量导入
            db.commit()
        except Exception:
            db.rollback()
            raise HTTPException(status_code=404, detail="保存失败")
        return db.query(NodeTempModel).filter_by(workflow_id=workflow_id).all()

    @staticmethod
    def publish(db: Session, workflow: models.WorkflowModel):
        workflow_id = workflow.id
        insert_objects = []
        node_user_mappings = []
        node_link_mappings = []
        target_node_ids = {"g0": 0}
        node_temps = db.query(NodeTempModel).filter_by(workflow_id=workflow_id).all()
        for item in node_temps:
            target_node_ids[item.target] = item.id
        for obj in node_temps:
            insert_objects.append({
                "id": obj.id,
                "workflow_id": workflow_id,
                "node_name": obj.node_name,
                "node_type": obj.node_type,
                "field": obj.field,
                "condition": obj.condition
            })
            source_data = json.loads(obj.source)
            for source in source_data:
                if source in target_node_ids:
                    node_link_mappings.append({
                        "workflow_id": workflow_id,
                        "pre_node_id": target_node_ids.get(source),
                        "next_node_id": obj.id,
                        "condition": obj.condition
                    })
            user_ids = json.loads(obj.user)
            for user_id in user_ids:
                node_user_mappings.append({"workflow_id": workflow_id, "node_id": obj.id, "user_id": user_id})
        try:
            db.query(NodeModel).filter_by(workflow_id=workflow_id).delete()
            db.query(NodeLinkModel).filter_by(workflow_id=workflow_id).delete()
            db.query(NodeUserModel).filter_by(workflow_id=workflow_id).delete()
            if insert_objects:
                db.bulk_insert_mappings(NodeModel, insert_objects)
            if node_user_mappings:
                db.bulk_insert_mappings(NodeUserModel, node_user_mappings)
            if node_link_mappings:
                db.bulk_insert_mappings(NodeLinkModel, node_link_mappings)
            # 批量导入
            db.commit()
        except Exception:
            db.rollback()
            raise HTTPException(status_code=404, detail="发布失败")
        return db.query(NodeTempModel).filter_by(workflow_id=workflow_id).all()




node = CRUDNode(NodeModel)
