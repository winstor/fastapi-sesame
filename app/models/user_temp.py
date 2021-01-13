from sqlalchemy import Boolean, Column, Integer, String, Text, SmallInteger
from app.db.database import Base
import uuid


def gen_id():
    return uuid.uuid4().hex


# 作用域 临时权限
# 指派类型 1地址+密码指派，3，地址+关联账号验证码，
class UserTempModel(Base):
    __tablename__ = "user_temps"

    id = Column(String(32), default=gen_id, primary_key=True, index=True, comment='主键')
    site_id = Column(Integer, default=0, index=True, comment='站点ID')
    from_user_id = Column(Integer, comment='指派人ID')
    to_user_id = Column(Integer, nullable=True, default=0, comment='被指派人ID')
    title = Column(String(100), nullable=True, comment='标题')
    scopes = Column(Text, comment='作用域,权限')
    hashed_password = Column(String, nullable=True, comment='hash密码')
    token = Column(String, nullable=True, comment='登录生成token')
    expire = Column(Integer, comment='到期时间')
    disabled = Column(Boolean, default=False, comment='是否禁用')
