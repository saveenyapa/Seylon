from datetime import datetime
from pydantic import BaseModel, HttpUrl, field_validator
from typing import Optional, Literal

VehicleTag = Literal["luxury", "vintage", "suv", "convertible"]


class VehicleBase(BaseModel):
    name: str
    sub: str
    tag: VehicleTag
    price: int
    image_url: str
    is_active: bool = True


class VehicleCreate(VehicleBase):
    pass


class VehicleUpdate(BaseModel):
    name: Optional[str] = None
    sub: Optional[str] = None
    tag: Optional[VehicleTag] = None
    price: Optional[int] = None
    image_url: Optional[str] = None
    is_active: Optional[bool] = None


class VehicleOut(VehicleBase):
    id: int
    created_at: datetime

    model_config = {"from_attributes": True}
