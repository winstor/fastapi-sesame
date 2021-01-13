from sqlalchemy import Column, Integer, String, SmallInteger
from app.api.workflow.db.database import Base


# 节点-用户关联表
class NodeUserModel(Base):
    __tablename__ = "wf_node_users"

    id = Column(Integer, primary_key=True, index=True, comment='主键')
    workflow_id = Column(Integer, index=True, comment="工作流程ID")
    node_id = Column(Integer, index=True, comment='流程节点ID')
    user_id = Column(Integer, index=True, comment='用户ID')
