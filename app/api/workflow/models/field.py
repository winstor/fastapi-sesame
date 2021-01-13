from sqlalchemy import Column, Integer, String, Text, SmallInteger, Boolean
from app.api.workflow.db.database import Base


# 流程表单设置
# fields = [{"name":"字段名称","default":"默认值","relation":{"workflow_id":"工作流程ID","form_field_id":"form字段ID"}}]
class FieldModel(Base):
    __tablename__ = "wf_fields"

    id = Column(Integer, primary_key=True, index=True, comment='主键')
    workflow_id = Column(Integer, index=True, comment='流程ID')
    field_name = Column(String, comment='字段名称')
    slug = Column(String(20), comment='类型')
    default = Column(Text, default='', comment='默认值')
    options = Column(Text, default='', nullable=True, comment="选项")
    relation_wid = Column(Integer, default=0, comment='关联流程ID')
    relation_fid = Column(Integer, default=0, comment='关联流程form id')
    order = Column(SmallInteger, comment='顺序')
    # is_delete = Column(Boolean, default=False, nullable=True, comment='是否删除')
