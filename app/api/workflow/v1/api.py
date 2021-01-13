from fastapi import APIRouter, Security
from .endpoints import field_cates, groups
from .endpoints import workflow_groups, workflows, field_settings, node, workflow_routers
from app.api.workflow import common
from .endpoints import workflow_apply

api_router = APIRouter()

# 字段类型 root 权限
api_router.include_router(field_cates.router, prefix='/field-type', tags=["字段类型"], dependencies=[
    Security(common.validate_scopes, scopes=["mgmt"])
])
# /////////////////////////////////////////////////////////////////////////////////////////
# 用户组管理
api_router.include_router(groups.router, prefix='/groups', tags=["用户组管理"], dependencies=[
    Security(common.validate_scopes, scopes=["mgmt"])
])

# 流程管理
api_router.include_router(workflow_groups.router, prefix='/workflow-groups', tags=["流程组管理"], dependencies=[
    Security(common.validate_scopes, scopes=["mgmt"])
])
api_router.include_router(workflows.router, prefix='/workflow', tags=["流程管理"], dependencies=[
    Security(common.validate_scopes, scopes=["mgmt"])
])
api_router.include_router(field_settings.router, prefix='/workflow-field', tags=["流程字段设置"], dependencies=[
    Security(common.validate_scopes, scopes=["mgmt"])
])

api_router.include_router(node.router, prefix='/workflow-node', tags=["节点设置"], dependencies=[
    Security(common.validate_scopes, scopes=["mgmt"])
])

api_router.include_router(workflow_routers.router, prefix='/workflow-routers', tags=["workflow routers"])
api_router.include_router(workflow_apply.router, prefix='/workflow-apply', tags=["workflow apply"])


# 节点管理
