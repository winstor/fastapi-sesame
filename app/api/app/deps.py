from app.api.deps import *
from fastapi import File, UploadFile, Header
from app.extensions import site_sign
from app import crud
from app import models


def get_current_site(db: Session = Depends(database.get_db), site_secret: str = Header(None)) -> models.SiteModel:
    if not site_secret:
        raise HTTPException(status_code=400, detail="Site-Secret not found")
    db_site = crud.site.get_by_secret(db, site_secret)
    if not db_site:
        raise HTTPException(status_code=400, detail="Site-Secret not found")
    return db_site


def get_auth_site(
        db: Session = Depends(database.get_db),
        secret: str = Depends(site_sign.sign_decode)
) -> models.SiteModel:
    site = crud.site.get_by_secret(db, secret)
    if not site:
        site = crud.site.get(db, secret)
    return site


def get_filter_file(file: UploadFile = File(...)):
    return file
