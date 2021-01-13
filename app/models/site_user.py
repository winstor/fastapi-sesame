import datetime
from sqlalchemy import Column, Integer, DateTime, Boolean, Text, UniqueConstraint
from app.db.database import Base


def gen_time():
    return datetime.datetime.now()


# 站点表: 某某高校
# 外键 uid
class SiteUserModel(Base):
    __tablename__ = "site_users"

    id = Column(Integer, primary_key=True, index=True, comment='用户ID')
    site_id = Column(Integer, default=0, index=True, comment='站点ID')
    user_id = Column(Integer, default=0, index=True, comment='用户ID')
    is_mgmt = Column(Boolean, default=False, nullable=True, comment='站点管理员')
    # type = Column(Integer, default=0, index=True, comment='用户类型:0 游客、申请用户，1正式成员')
    disabled = Column(Boolean, default=False, comment='是否禁用')
    app_scopes = Column(Text, default='', comment='应用作用域')
    end_time = Column(DateTime, default=False, comment='账号结束时间')
    created_at = Column(DateTime, default=gen_time, comment='创建时间')
    __table_args__ = (
        UniqueConstraint('site_id', "user_id", name="users_site_id_user_id_unique"),
    )
