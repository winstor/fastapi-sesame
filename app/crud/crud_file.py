from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.file import FileModel


class CRUDFile(CRUDBase[FileModel]):
    def get_by_path(self, db: Session, path: str) -> FileModel:
        return db.query(self.model).filter(self.model.path == path).first()


file = CRUDFile(FileModel)
