from datetime import date
from typing import Optional

from sqlalchemy.orm import Session

from app import models, schemas


def get_assets(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    status: Optional[models.AssetStatus] = None,
    department: Optional[str] = None,
):
    query = db.query(models.Asset)
    if status:
        query = query.filter(models.Asset.status == status)
    if department:
        query = query.filter(models.Asset.department == department)
    return query.offset(skip).limit(limit).all()


def get_asset(db: Session, asset_id: int):
    return db.query(models.Asset).filter(models.Asset.id == asset_id).first()


def create_asset(db: Session, asset: schemas.AssetCreate):
    db_asset = models.Asset(**asset.model_dump())
    db.add(db_asset)
    db.commit()
    db.refresh(db_asset)
    return db_asset


def update_asset(db: Session, asset_id: int, asset: schemas.AssetUpdate):
    db_asset = get_asset(db, asset_id)
    if not db_asset:
        return None
    for field, value in asset.model_dump(exclude_unset=True).items():
        setattr(db_asset, field, value)
    db.commit()
    db.refresh(db_asset)
    return db_asset


def delete_asset(db: Session, asset_id: int):
    db_asset = get_asset(db, asset_id)
    if not db_asset:
        return False
    db.delete(db_asset)
    db.commit()
    return True


def get_expiring_warranties(db: Session, within_days: int = 30):
    from datetime import timedelta

    deadline = date.today() + timedelta(days=within_days)
    return (
        db.query(models.Asset)
        .filter(models.Asset.warranty_until.isnot(None))
        .filter(models.Asset.warranty_until <= deadline)
        .filter(models.Asset.warranty_until >= date.today())
        .all()
    )
