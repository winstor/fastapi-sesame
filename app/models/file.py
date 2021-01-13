import time
from sqlalchemy import Column, Integer, String
from app.db.database import Base


def gen_date():
    return int(time.time())


# 站点表: 某某高校
# 外键 site_id
class FileModel(Base):
    __tablename__ = "sys_files"

    id = Column(Integer, primary_key=True, index=True, comment='站点ID')
    site_id = Column(Integer, default=0, index=True, comment='站点ID')
    user_id = Column(Integer, default=0, index=True, comment='用户ID')
    name = Column(String, comment='文件名称')
    path = Column(String, unique=True, index=True, comment='文件路径')
    type = Column(String(50), comment='文件类型')
    size = Column(Integer, comment='大小')
    date = Column(Integer, default=gen_date, comment='创建时间')
