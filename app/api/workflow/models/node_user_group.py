from sqlalchemy import Column, Integer
from app.api.workflow.db.database import Base


# 节点-用户组关联表
class NodeUserGroupModel(Base):
    __tablename__ = "wf_node_group_users"

    id = Column(Integer, primary_key=True, index=True, comment='主键')
    workflow_id = Column(Integer, index=True, comment="工作流程ID")
    node_id = Column(Integer, index=True, comment='流程节点ID')
    group_id = Column(Integer, index=True, comment='用户组ID')
