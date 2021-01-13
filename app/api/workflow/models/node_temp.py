from sqlalchemy import Boolean, Column, Integer, DateTime, Text, SmallInteger, String
import datetime
from app.api.workflow.db.database import Base


# 流程节点表
class NodeTempModel(Base):
    __tablename__ = "wf_node_temps"

    id = Column(Integer, primary_key=True, index=True, comment='主键')
    workflow_id = Column(Integer, index=True, comment="工作流程ID")
    node_name = Column(String(50), nullable=False, comment='节点名称')
    source = Column(Text, default='', nullable=False, comment='source')
    target = Column(String, default='', nullable=False, comment='target')
    node_type = Column(String(10), comment='节点类型：start起始节点，review审批节点，task任务节点，suspend阻塞节点，end结束节点')
    # edges = Column(Text, default='', nullable=True, comment="连线数据")  # [{}]
    field = Column(Text, default='', nullable=True, comment="字段信息")  # [{id:state,1:1}]  state 0 隐藏 1显示，2编辑
    user = Column(Text, default='', nullable=True, comment="用户数据")  # [{}]
    user_group = Column(Text, default='', nullable=True, comment="用户组数据")  # [{}]
    extend_data = Column(Text, default='', nullable=True, comment="节点数据")
    condition = Column(String, default='', nullable=True, comment="阻塞条件")  # [{}]
    create_user = Column(String(30), nullable=True, comment='创建人')
    created_at = Column(DateTime, default=datetime.datetime.now, comment='创建时间')

    # 把SQLAlchemy查询对象转换成字典
    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
