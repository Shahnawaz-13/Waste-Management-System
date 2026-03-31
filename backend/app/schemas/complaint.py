from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from app.models.enums import ComplaintStatus, WasteClass


class Location(BaseModel):
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    address: Optional[str] = None


class ComplaintCreate(BaseModel):
    user_id: str
    description: str = Field(..., min_length=10)
    location: Location


class ComplaintInDB(ComplaintCreate):
    id: str
    image_url: str
    predicted_class: WasteClass
    status: ComplaintStatus = ComplaintStatus.PENDING
    assigned_worker_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime


class ComplaintStatusUpdate(BaseModel):
    status: ComplaintStatus


class TaskAssignRequest(BaseModel):
    worker_id: str
