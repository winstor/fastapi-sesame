from fastapi import APIRouter, Depends
from .files import files, sigin_files
from app.core import request_sign


api_router = APIRouter()


api_router.include_router(
    files.router,
    prefix='/files',
    tags=["files"],
)

api_router.include_router(
    sigin_files.router,
    prefix='/files',
    tags=["files"],
    dependencies=[Depends(request_sign.check_site_sign)]
)
