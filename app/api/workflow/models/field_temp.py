from sqlalchemy import Column, Integer, String, Text, SmallInteger, Boolean
from app.api.workflow.db.database import Base


class FieldTempModel(Base):
    __tablename__ = "wf_field_temps"

    id = Column(Integer, primary_key=True, index=True, comment='主键')
    workflow_id = Column(Integer, index=True, comment='流程ID')
    field_name = Column(String, comment='字段名称')
    slug = Column(String(20), comment='类型')
    default = Column(Text, default='', comment='默认值')
    options = Column(Text, default='', nullable=True, comment="选项")
    relation_wid = Column(Integer, default=0, comment='关联流程ID')
    relation_fid = Column(Integer, default=0, comment='关联流程form id')
    order = Column(SmallInteger, comment='顺序')

    # 把SQLAlchemy查询对象转换成字典
    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
