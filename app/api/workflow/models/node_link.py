from sqlalchemy import Boolean, Column, Integer, DateTime, Text, SmallInteger, String
import datetime
from app.api.workflow.db.database import Base


# 流程线路表
class NodeLinkModel(Base):
    __tablename__ = "wf_node_links"

    id = Column(Integer, primary_key=True, index=True, comment='主键')
    workflow_id = Column(Integer, index=True, comment="工作流程ID")
    pre_node_id = Column(Integer, comment='上一流程节点')
    next_node_id = Column(Integer, comment='下一流程节点')
    condition = Column(String, default='', nullable=True, comment="阻塞条件")


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
