from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class PackageFeatureOut(BaseModel):
    id: int
    text: str
    included: bool
    sort_order: int

    model_config = {"from_attributes": True}


class PackageFeatureCreate(BaseModel):
    text: str
    included: bool = True
    sort_order: int = 0


class PackageBase(BaseModel):
    name: str
    slug: str
    hours: int
    description: str
    price: int
    is_featured: bool = False
    is_active: bool = True


class PackageCreate(PackageBase):
    features: list[PackageFeatureCreate] = []


class PackageOut(PackageBase):
    id: int
    created_at: datetime
    features: list[PackageFeatureOut] = []

    model_config = {"from_attributes": True}
