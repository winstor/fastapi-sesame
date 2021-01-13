import datetime
from sqlalchemy import Column, Integer, DateTime, Boolean, Text, UniqueConstraint, String
from app.db.database import Base


def gen_time():
    return datetime.datetime.now()


# 站点表: 某某高校
# 外键 uid
class OrgUserModel(Base):
    __tablename__ = "org_users"

    id = Column(Integer, primary_key=True, index=True, comment='用户ID')
    org_id = Column(Integer, index=True, comment='站点ID')
    username = Column(String(64), unique=True, index=True, nullable=True, comment='登录账号')
    hashed_password = Column(String(64), nullable=True, comment='登录密码')
    user_id = Column(Integer, default=0, index=True, comment='用户ID')
    is_mgmt = Column(Boolean, default=False, nullable=True, comment='站点管理员')
    disabled = Column(Boolean, default=False, comment='是否禁用')
    end_time = Column(DateTime, default=False, comment='账号结束时间')
    created_at = Column(DateTime, default=gen_time, comment='创建时间')
    # __table_args__ = (
    #     UniqueConstraint('org_id', "user_id", name="org_users_org_id_user_id_unique"),
    # )
