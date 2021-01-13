from typing import Optional
from fastapi import Depends, APIRouter, Depends, HTTPException, status, File, UploadFile

router = APIRouter()


@router.delete('/delete')
async def delete_file(paths: Optional[list]):
    return paths
