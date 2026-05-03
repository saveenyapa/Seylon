import re
from datetime import datetime, date
from pydantic import BaseModel, field_validator, model_validator
from typing import Optional
from app.models.enquiry import EnquiryStatus
from app.schemas.vehicle import VehicleOut

_TIME_RE = re.compile(r"^\d{2}:\d{2}$")
_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


class EnquiryCreate(BaseModel):
    full_name: str
    phone: str
    wedding_date: str           # "YYYY-MM-DD"
    vehicle_id: Optional[int] = None
    pickup_time: str            # "HH:MM"
    return_time: str            # "HH:MM"
    notes: Optional[str] = None

    @field_validator("full_name")
    @classmethod
    def name_not_empty(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("full_name must not be empty")
        return v

    @field_validator("phone")
    @classmethod
    def phone_not_empty(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("phone must not be empty")
        return v

    @field_validator("wedding_date")
    @classmethod
    def validate_date(cls, v: str) -> str:
        if not _DATE_RE.match(v):
            raise ValueError("wedding_date must be in YYYY-MM-DD format")
        # Must not be in the past
        if date.fromisoformat(v) < date.today():
            raise ValueError("wedding_date must be today or a future date")
        return v

    @field_validator("pickup_time", "return_time")
    @classmethod
    def validate_time(cls, v: str) -> str:
        if not _TIME_RE.match(v):
            raise ValueError("Time must be in HH:MM format")
        return v


class EnquiryStatusUpdate(BaseModel):
    status: EnquiryStatus


class EnquiryOut(BaseModel):
    id: int
    full_name: str
    phone: str
    wedding_date: str
    vehicle_id: Optional[int]
    vehicle: Optional[VehicleOut] = None
    pickup_time: str
    return_time: str
    notes: Optional[str]
    status: EnquiryStatus
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class EnquiryListOut(BaseModel):
    total: int
    items: list[EnquiryOut]
