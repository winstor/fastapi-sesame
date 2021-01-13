from typing import Any, Optional, TypeVar, Type
from fastapi import HTTPException
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from app.config import database as config_database

# SQLALCHEMY_DATABASE_URL = "postgresql://postgres:jwb123@localhost:5432/workflow"

Base = declarative_base()

ModelType = TypeVar("ModelType", bound=Base)


class DB:
    engine: Any = ''
    session_local: Any = ''

    def __init__(self, name: Optional[str] = None):
        if name:
            self.set_default_connection(name)

    def get_db(self):
        s_db = self.get_session()
        try:
            yield s_db
        finally:
            s_db.close()

    def get_session(self) -> Session:
        if not self.session_local:
            raise HTTPException(status_code=401, detail='数据库驱动不存在')
        return self.session_local()

    def query(self, model: Type[ModelType]):
        return self.get_session().query(model)

    def create_all(self, base):
        if not self.engine:
            raise HTTPException(status_code=401, detail='数据库驱动不存在')
        base.metadata.create_all(bind=self.engine)

    #
    def create_engine(self, database_url: Optional[str], **kwargs):
        self.engine = create_engine(database_url, **kwargs)
        self.session_local = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        return self
        # pool_pre_ping=True

    def configuration(self, database_url: Optional[str], **kwargs):
        self.engine = create_engine(database_url, **kwargs)
        self.session_local = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        return self

    def set_default_connection(self, name: Optional[str] = None):
        if not name:
            name = config_database.default
        database_url = config_database.connections.get(name).get("url")
        kwargs = config_database.connections.get(name).get("kwargs")
        self.create_engine(database_url, **kwargs)
        return self

    @staticmethod
    def connection(name: Optional[str] = None):
        if not name:
            name = config_database.default
        return DB(name)


database = DB()
