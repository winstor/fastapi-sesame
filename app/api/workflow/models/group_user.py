from sqlalchemy import Column, Integer, String
from app.api.workflow.db.database import Base


# 用户组-用户关联表
class GroupUserModel(Base):
    __tablename__ = "wf_group_users"

    id = Column(Integer, primary_key=True, index=True, comment='主键')
    group_id = Column(Integer, index=True, comment='用户组ID')
    user_id = Column(Integer, index=True, comment='用户ID')
    user_name = Column(String, nullable=True, comment='用户名')
