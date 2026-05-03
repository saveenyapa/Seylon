from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.vehicle import VehicleOut, VehicleCreate, VehicleUpdate
from app.services import vehicle_service

router = APIRouter(prefix="/vehicles", tags=["Vehicles"])


@router.get("/", response_model=List[VehicleOut], summary="List all active vehicles")
def list_vehicles(
    tag: Optional[str] = Query(None, description="Filter by tag: luxury|vintage|suv|convertible"),
    max_price: Optional[int] = Query(None, ge=0, description="Maximum price (LKR) filter"),
    db: Session = Depends(get_db),
):
    return vehicle_service.get_all(db, tag=tag, max_price=max_price)


@router.get("/{vehicle_id}", response_model=VehicleOut, summary="Get a single vehicle")
def get_vehicle(vehicle_id: int, db: Session = Depends(get_db)):
    vehicle = vehicle_service.get_by_id(db, vehicle_id)
    if not vehicle:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vehicle not found")
    return vehicle


@router.post("/", response_model=VehicleOut, status_code=status.HTTP_201_CREATED, summary="Create a vehicle")
def create_vehicle(payload: VehicleCreate, db: Session = Depends(get_db)):
    return vehicle_service.create(db, payload)


@router.patch("/{vehicle_id}", response_model=VehicleOut, summary="Partially update a vehicle")
def update_vehicle(vehicle_id: int, payload: VehicleUpdate, db: Session = Depends(get_db)):
    vehicle = vehicle_service.update(db, vehicle_id, payload)
    if not vehicle:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vehicle not found")
    return vehicle


@router.delete("/{vehicle_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete a vehicle")
def delete_vehicle(vehicle_id: int, db: Session = Depends(get_db)):
    deleted = vehicle_service.delete(db, vehicle_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vehicle not found")
