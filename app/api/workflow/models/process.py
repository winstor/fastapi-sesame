from sqlalchemy import Column, Integer, DateTime, Text, SmallInteger, String
import datetime
from app.api.workflow.db.database import Base


# 流程进度
class ProgressModel(Base):
    __tablename__ = "wf_progress"

    id = Column(Integer, primary_key=True, index=True, comment='主键')
    workflow_id = Column(Integer, index=True, comment="工作流程ID")
    curr_node_id = Column(Integer, comment='当前节点ID')
    deal_state = Column(SmallInteger, default=1, comment="1-未结束，2-结束")
    create_user = Column(String(30), nullable=True, comment='创建人')
    created_at = Column(DateTime, default=datetime.datetime.now, comment='创建时间')
