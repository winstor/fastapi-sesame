from sqlalchemy import Boolean, Column, Integer, DateTime, Text, SmallInteger, String
import datetime
from app.api.workflow.db.database import Base


# 流程节点表
class NodeModel(Base):
    __tablename__ = "wf_nodes"

    id = Column(Integer, primary_key=True, index=True, comment='主键')
    workflow_id = Column(Integer, index=True, comment="工作流程ID")
    node_type = Column(SmallInteger, default=0, comment='节点类型：0起始节点，1任务节点，2审批节点，3阻塞节点，4结束节点')
    node_name = Column(String(50), nullable=False, comment='节点名称')
    field = Column(Text, default='', nullable=True, comment="字段信息")  # [{id:1,state:1}]  state 0 隐藏 1显示，2编辑
    condition = Column(String, default='', nullable=True, comment="阻塞条件")
    create_user = Column(String(30), nullable=True, comment='创建人')
    created_at = Column(DateTime, default=datetime.datetime.now, comment='创建时间')


'''
# 流程节点


node_id	varchar(20)	是	流程节点id，用来标识流程节点
workflow_id	varchar(20)	否	流程id，用来标识流程和节点的关系
node_name	varchar(100)	否	节点名称
node_status	varchar(1)	否	流程节点状态，1-起始节点，2-流程中间节点，3-结束节点
create_time	datetime	否	创建时间
create_user	varchar(20)	否	创建人




'''
