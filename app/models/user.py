from sqlalchemy import Boolean, Column, Integer, String, DateTime, SmallInteger
from app.db.database import Base
import datetime


def gen_time():
    return datetime.datetime.now()


# 用户表
# 外键 user_id
class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, comment='用户ID')
    org_id = Column(Integer, default=0, index=True, comment='组织ID')
    username = Column(String(64), unique=True, index=True, nullable=True, comment='登录账号')
    wx_openid = Column(String(64), unique=True, index=True, nullable=True, comment='微信openid')
    mobile = Column(String(20), nullable=True, comment='电话')
    email = Column(String(64), nullable=True, comment='邮箱')
    hashed_password = Column(String(64), nullable=True, comment='登录密码')
    name = Column(String(64), nullable=True, comment='姓名')
    qq = Column(String(20), nullable=True, comment='qq')
    wechat_number = Column(String(64), nullable=True, comment='微信号')
    avatar = Column(String, nullable=True, comment='头像')
    type = Column(SmallInteger, default=0, comment='账号类型0(普通)1(高校)2(企业)')
    is_employee = Column(Boolean, default=False, nullable=True, comment='员工')
    is_root = Column(Boolean, default=False, nullable=True, comment='管理员')

    disabled = Column(Boolean, default=False, comment='是否禁用')
    created_at = Column(DateTime, default=gen_time, comment='创建时间')

    # 把SQLAlchemy查询对象转换成字典
    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
