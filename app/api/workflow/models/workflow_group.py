from sqlalchemy import Column, Integer, String
from app.api.workflow.db.database import Base


# workflow 流程应用
class WorkflowGroupModel(Base):
    __tablename__ = "wf_workflow_groups"

    id = Column(Integer, primary_key=True, index=True, comment='主键')
    site_id = Column(Integer, default=0, index=True, comment='站点ID')
    creator_id = Column(Integer, default=0, index=True, comment='创建人ID')
    name = Column(String(50), comment='应用名称')
