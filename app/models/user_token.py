from sqlalchemy import Boolean, Column, Integer, String, Text, SmallInteger
from app.db.database import Base
import uuid


class UserTokenModel(Base):
    __tablename__ = "user_tokens"

    id = Column(Integer, primary_key=True, index=True, comment='主键')
    user_id = Column(Integer, default=0, comment='用户ID')
    token = Column(String(150), unique=True, index=True, comment='登录生成token')
    scopes = Column(Text, comment='作用域,权限')
    expire = Column(Integer, comment='到期时间')
