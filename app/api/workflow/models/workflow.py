from sqlalchemy import Column, Integer, String, DateTime
from app.api.workflow.db.database import Base
import datetime


# workflow工作流程 流程表
class WorkflowModel(Base):
    __tablename__ = "wf_workflows"

    id = Column(Integer, primary_key=True, index=True, comment='主键')
    site_id = Column(Integer, index=True, comment='站点ID')
    group_id = Column(Integer, index=True, comment="流程组ID")
    workflow_name = Column(String(50), comment='流程名称')
    creator_id = Column(Integer, default=0, index=True, comment='创建人ID')
    created_at = Column(DateTime, default=datetime.datetime.now, comment='创建时间')
    updated_at = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now, comment='更新时间')


'''

workflow_id	varchar(20)	是	流程id，流程识别时的唯一标识	 	 	 
workflow_name	varchar(100)	否	流程名称	 	 	 
create_time	datetime	否	创建时间	 	 	 
create_user	varchar(20)	否	创建人



'''
