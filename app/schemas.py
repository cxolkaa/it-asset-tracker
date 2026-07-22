from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from app.models import AssetStatus, AssetType


class AssetBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=120)
    asset_type: AssetType = AssetType.OTHER
    serial_number: Optional[str] = Field(None, max_length=80)
    assigned_to: Optional[str] = Field(None, max_length=120)
    department: Optional[str] = Field(None, max_length=80)
    status: AssetStatus = AssetStatus.ACTIVE
    purchase_date: Optional[date] = None
    warranty_until: Optional[date] = None
    notes: Optional[str] = None


class AssetCreate(AssetBase):
    pass


class AssetUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=120)
    asset_type: Optional[AssetType] = None
    serial_number: Optional[str] = Field(None, max_length=80)
    assigned_to: Optional[str] = Field(None, max_length=120)
    department: Optional[str] = Field(None, max_length=80)
    status: Optional[AssetStatus] = None
    purchase_date: Optional[date] = None
    warranty_until: Optional[date] = None
    notes: Optional[str] = None


class AssetResponse(AssetBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime
