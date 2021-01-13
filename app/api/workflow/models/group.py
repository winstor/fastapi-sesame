from sqlalchemy import Column, Integer, String
from app.api.workflow.db.database import Base


# 用户组表
class GroupModel(Base):
    __tablename__ = "wf_groups"

    id = Column(Integer, primary_key=True, index=True, comment='主键')
    site_id = Column(Integer, index=True, comment='站点ID')
    name = Column(String(50), comment='用户组名称')
