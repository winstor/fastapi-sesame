from sqlalchemy import Boolean, Column, Integer, DateTime, Text, SmallInteger, String
import datetime
from app.api.workflow.db.database import Base


# 流程申请表
class ApplyModel(Base):
    __tablename__ = "wf_applies"

    id = Column(Integer, primary_key=True, index=True, comment='主键')
    title = Column(String, nullable=False, comment='标题')
    workflow_id = Column(Integer, index=True, comment="工作流程ID")
    data = Column(Text, default='', comment='内容')
    state = Column(SmallInteger, index=True, default=1, comment='1-未结束，2-结束')
    creator_id = Column(Integer, index=True, comment='申请人、创建人')
    create_user = Column(String(30), nullable=True, comment='创建人')
    created_at = Column(DateTime, default=datetime.datetime.now, comment='创建时间')


'''

workflow_id	varchar(20)	是	流程id，流程识别时的唯一标识	 	 	 
workflow_name	varchar(100)	否	流程名称	 	 	 
create_time	datetime	否	创建时间	 	 	 
create_user	varchar(20)	否	创建人



'''
