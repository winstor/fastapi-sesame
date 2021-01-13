from sqlalchemy import Boolean, Column, Integer, String, DateTime, Text, UniqueConstraint
from app.db.database import Base
import datetime


def gen_time():
    return datetime.datetime.now()


# 用户表
# 外键 user_id
class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, comment='用户ID')
    site_id = Column(Integer, default=0, index=True, comment='站点ID')
    username = Column(String(64), nullable=True, comment='登录账号')
    wx_openid = Column(String(64), nullable=True, comment='微信openid')
    mobile = Column(String(20), nullable=True, comment='电话')
    email = Column(String(64), nullable=True, comment='邮箱')
    hashed_password = Column(String(64), nullable=True, comment='hash登录密码')
    name = Column(String(64), nullable=True, comment='姓名')
    avatar = Column(String, nullable=True, comment='头像')
    is_root = Column(Boolean, default=False, nullable=True, comment='根管理员')
    is_mgmt = Column(Boolean, default=False, nullable=True, comment='站点管理员')
    disabled = Column(Boolean, default=False, comment='是否禁用')
    app_scopes = Column(Text, default='', comment='应用作用域')
    end_time = Column(DateTime, nullable=True, comment='账号结束时间')
    created_at = Column(DateTime, default=gen_time, comment='创建时间')
    __table_args__ = (
        UniqueConstraint('site_id', "wx_openid", name="users_site_id_wx_openid_unique"),
        UniqueConstraint('site_id', "username", name="users_site_id_username_unique"),
    )

    # 把SQLAlchemy查询对象转换成字典
    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
