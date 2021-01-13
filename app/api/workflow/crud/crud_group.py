from app.crud.base import CRUDBase
from app.api.workflow.models import GroupModel


class CRUDGroup(CRUDBase):
    pass


group = CRUDGroup(GroupModel)

crud = {"name": group}
