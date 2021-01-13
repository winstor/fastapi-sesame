import time
import json
from app.models import CacheModel
from sqlalchemy.orm import Session


class Cache:
    db: Session

    def __init__(self, db: Session = None):
        if db:
            self.db = db

    def set_db(self, db: Session):
        self.db = db
        return self

    def get(self, key: str):
        res = self.db.query(CacheModel).filter(CacheModel.id == key).first()
        if res:
            now = int(time.time())
            if now < res.expire_at:
                return json.loads(res.data)
            else:
                self.db.query(CacheModel).filter(CacheModel.expire_at < now).delete()
        return False

    def put(self, key: str, value, minute: int):
        self.db.query(CacheModel).filter(CacheModel.id == key).delete()
        if value:
            expire_at = int(time.time()) + int(minute) * 60
            data = json.dumps(value)
            db_cache = CacheModel(id=key, data=data, expire_at=expire_at)
            self.db.add(db_cache)
            self.db.commit()
            self.db.refresh(db_cache)
            self.db.close()


cache = Cache()
