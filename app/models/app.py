from sqlalchemy import Boolean, Column, Integer, String
from app.db.database import Base


# application应用 如聊天app，高校app，财务app
class AppModel(Base):
    __tablename__ = "apps"

    id = Column(Integer, primary_key=True, index=True, comment='主键')
    name = Column(String(50), comment='应用名称')

