from typing import List, Optional

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.database import Base, engine, get_db

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="IT Asset Tracker",
    description="REST API for tracking company hardware, licenses, and warranties.",
    version="1.0.0",
)


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/assets", response_model=List[schemas.AssetResponse])
def list_assets(
    skip: int = 0,
    limit: int = Query(100, le=500),
    status: Optional[models.AssetStatus] = None,
    department: Optional[str] = None,
    db: Session = Depends(get_db),
):
    return crud.get_assets(db, skip=skip, limit=limit, status=status, department=department)


@app.get("/assets/warranties/expiring", response_model=List[schemas.AssetResponse])
def expiring_warranties(
    days: int = Query(30, ge=1, le=365),
    db: Session = Depends(get_db),
):
    return crud.get_expiring_warranties(db, within_days=days)


@app.get("/assets/{asset_id}", response_model=schemas.AssetResponse)
def get_asset(asset_id: int, db: Session = Depends(get_db)):
    asset = crud.get_asset(db, asset_id)
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    return asset


@app.post("/assets", response_model=schemas.AssetResponse, status_code=201)
def create_asset(asset: schemas.AssetCreate, db: Session = Depends(get_db)):
    if asset.serial_number:
        existing = (
            db.query(models.Asset)
            .filter(models.Asset.serial_number == asset.serial_number)
            .first()
        )
        if existing:
            raise HTTPException(status_code=409, detail="Serial number already exists")
    return crud.create_asset(db, asset)


@app.patch("/assets/{asset_id}", response_model=schemas.AssetResponse)
def update_asset(
    asset_id: int, asset: schemas.AssetUpdate, db: Session = Depends(get_db)
):
    updated = crud.update_asset(db, asset_id, asset)
    if not updated:
        raise HTTPException(status_code=404, detail="Asset not found")
    return updated


@app.delete("/assets/{asset_id}", status_code=204)
def delete_asset(asset_id: int, db: Session = Depends(get_db)):
    if not crud.delete_asset(db, asset_id):
        raise HTTPException(status_code=404, detail="Asset not found")
