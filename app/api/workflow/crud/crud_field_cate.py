from app.crud.base import CRUDBase
from app.api.workflow.models import FieldCateModel


class CRUDFieldCate(CRUDBase):
    pass


field_cate = CRUDFieldCate(FieldCateModel)
