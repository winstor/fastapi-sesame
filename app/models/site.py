import uuid
import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime
from app.db.database import Base


def gen_secret():
    return uuid.uuid1().hex


def gen_time():
    return datetime.datetime.now()


# 站点表: 某某高校
# 外键 site_id
class SiteModel(Base):
    __tablename__ = "sites"

    id = Column(Integer, primary_key=True, index=True, comment='站点ID')
    parent_site_id = Column(Integer, default=0, index=True, comment='父站点ID')
    site_name = Column(String(64), unique=True, comment='站点名称')
    secret = Column(String(64), unique=True, index=True, default=gen_secret, comment='密钥')
    db_connect = Column(Text, default='', comment='数据库连接数据')
    verify_code = Column(String(20), default='', comment='用户加入验证码')
    description = Column(String(191), nullable=True, comment='描述')
    created_at = Column(DateTime, default=gen_time, comment='创建时间')
