from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import select, and_

from app.models.vehicle import Vehicle
from app.schemas.vehicle import VehicleCreate, VehicleUpdate


def get_all(
    db: Session,
    *,
    tag: Optional[str] = None,
    max_price: Optional[int] = None,
    active_only: bool = True,
) -> List[Vehicle]:
    """Return vehicles, optionally filtered by tag and/or max price."""
    conditions = []
    if active_only:
        conditions.append(Vehicle.is_active == True)
    if tag and tag != "all":
        conditions.append(Vehicle.tag == tag)
    if max_price is not None:
        conditions.append(Vehicle.price <= max_price)

    stmt = select(Vehicle).where(and_(*conditions)).order_by(Vehicle.id)
    return list(db.scalars(stmt).all())


def get_by_id(db: Session, vehicle_id: int) -> Optional[Vehicle]:
    return db.get(Vehicle, vehicle_id)


def create(db: Session, payload: VehicleCreate) -> Vehicle:
    vehicle = Vehicle(**payload.model_dump())
    db.add(vehicle)
    db.commit()
    db.refresh(vehicle)
    return vehicle


def update(db: Session, vehicle_id: int, payload: VehicleUpdate) -> Optional[Vehicle]:
    vehicle = db.get(Vehicle, vehicle_id)
    if not vehicle:
        return None
    data = payload.model_dump(exclude_unset=True)
    for key, value in data.items():
        setattr(vehicle, key, value)
    db.commit()
    db.refresh(vehicle)
    return vehicle


def delete(db: Session, vehicle_id: int) -> bool:
    vehicle = db.get(Vehicle, vehicle_id)
    if not vehicle:
        return False
    db.delete(vehicle)
    db.commit()
    return True
