from sqlalchemy import Boolean, Column, Integer, DateTime, Text, SmallInteger, String
import datetime
from app.api.workflow.db.database import Base


# 流程进展记录
class ProgressHistoryModel(Base):
    __tablename__ = "wf_progress_history"

    id = Column(Integer, primary_key=True, index=True, comment='主键')
    workflow_id = Column(Integer, index=True, comment="工作流程ID")
    progress_id = Column(Integer, index=True, comment="进度ID")
    curr_node_id = Column(Integer, index=True, comment='当前节点ID')
    curr_node_name = Column(String(50), nullable=False, comment='节点名称')
    node_action = Column(String(30), comment="通过-next,驳回-back,提交-submit")
    deal_user_id = Column(Integer, comment='当前节点处理人id')
    deal_user = Column(String(30), nullable=True, comment='当前节点处理人')
    deal_remark = Column(String(30), nullable=True, comment='当前节点操作备注')
    deal_time = Column(DateTime, default=datetime.datetime.now, comment='处理时间')
    create_user = Column(String(30), nullable=True, comment='创建人')


'''

t_workflow_node_link流程节点流向表

列名	类型	是否主键	描述
workflow_id	varchar(20)	是	流程id
curr_node_id	varchar(20)	是	当前流程节点
next_node_id	varchar(20)	是	下一流程节点
action_name	varchar(100)	否	流程流转描述
action	varchar(20)	否	流程流转标识,通过-next,驳回-back，用来标识此流转是通过还是驳回
workflow_status	varchar(10)	否	此步骤是否结束流程1-不结束，2-结束


'''
