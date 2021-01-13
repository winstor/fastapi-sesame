from sqlalchemy import Boolean, Column, Integer, String, DateTime, Text, UniqueConstraint
import datetime
from app.api.workflow.db.database import Base


def gen_time():
    return datetime.datetime.now()


# 申请表扩展
class ApplyExtendModel(Base):
    __tablename__ = "wf_apply_extends"

    id = Column(Integer, primary_key=True, index=True, comment='主键')
    apply_id = Column(Integer, index=True, comment="申请表ID")
    field_id = Column(Integer, index=True, comment='字段ID')
    value = Column(Text, default='', comment='相关字段值')
    __table_args__ = (
        UniqueConstraint('apply_id', "field_id", name="apply_id_field_id_unique"),
    )


'''

workflow_id	varchar(20)	是	流程id，流程识别时的唯一标识	 	 	 
workflow_name	varchar(100)	否	流程名称	 	 	 
create_time	datetime	否	创建时间	 	 	 
create_user	varchar(20)	否	创建人



'''
