from sqlalchemy import Column, Integer, String, SmallInteger
from app.api.workflow.db.database import Base


# 字段类型
# input file select radio checkbox 等 单行，多行，单文件，多文件，编辑器， 复选框，单选框，列表选择
class FieldCateModel(Base):
    __tablename__ = "wf_field_categories"

    id = Column(Integer, primary_key=True, index=True, comment='主键')
    field_cname = Column(String(50), comment='字段名称')
    slug = Column(String(20), unique=True, index=True, comment='标识')
    type = Column(SmallInteger, default=1, comment='1简单类型，2复合类型等')
