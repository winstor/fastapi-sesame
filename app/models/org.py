import uuid
import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, SmallInteger
from app.db.database import Base


def gen_secret():
    return uuid.uuid1().hex


def gen_time():
    return datetime.datetime.now()


# 组织表: 某某高校
# 外键 org_id
class OrgModel(Base):
    __tablename__ = "organizations"

    id = Column(Integer, primary_key=True, index=True, comment='组织ID')
    parent_org_id = Column(Integer, default=0, index=True, comment='父站组织ID')
    name = Column(String(64), unique=True, comment='组织名称')
    mobile = Column(String(20), nullable=True, comment='电话')
    email = Column(String(64), nullable=True, comment='邮箱')
    qq = Column(String(20), nullable=True, comment='qq')
    logo = Column(String, nullable=True, comment='logo')
    secret = Column(String(64), unique=True, index=True, default=gen_secret, comment='密钥')
    db_connect = Column(Text, default='', comment='数据库连接数据')
    verify_code = Column(String(20), default='', comment='用户加入验证码')
    type = Column(SmallInteger, default=1, comment='1(高校)2(企业)')
    description = Column(String(191), nullable=True, comment='描述')
    created_at = Column(DateTime, default=gen_time, comment='创建时间')
