from app.api.workflow import models
from .crud_field_cate import field_cate
from .crud_workflow_group import workflow_group
from .crud_field import field
from .crud_field_temp import field_temp
from .crud_workflow import workflow
from app.crud.base import CRUDBase
from .crud_node import node

node_temp = CRUDBase(models.NodeTempModel)

node_link = CRUDBase(models.NodeLinkModel)
node_user = CRUDBase(models.NodeUserModel)
node_user_group = CRUDBase(models.NodeUserGroupModel)

workflow_apply = CRUDBase(models.ApplyModel)
