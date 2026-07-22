import enum
from datetime import date, datetime

from sqlalchemy import Column, Date, DateTime, Enum, Integer, String, Text

from app.database import Base


class AssetStatus(str, enum.Enum):
    ACTIVE = "active"
    IN_REPAIR = "in_repair"
    RETIRED = "retired"
    LOST = "lost"


class AssetType(str, enum.Enum):
    LAPTOP = "laptop"
    DESKTOP = "desktop"
    SERVER = "server"
    MONITOR = "monitor"
    PRINTER = "printer"
    LICENSE = "license"
    OTHER = "other"


class Asset(Base):
    __tablename__ = "assets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(120), nullable=False)
    asset_type = Column(Enum(AssetType), nullable=False, default=AssetType.OTHER)
    serial_number = Column(String(80), unique=True, index=True)
    assigned_to = Column(String(120))
    department = Column(String(80))
    status = Column(Enum(AssetStatus), nullable=False, default=AssetStatus.ACTIVE)
    purchase_date = Column(Date)
    warranty_until = Column(Date)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
