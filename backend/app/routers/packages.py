from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.package import PackageOut, PackageCreate
from app.services import package_service

router = APIRouter(prefix="/packages", tags=["Packages"])


@router.get("/", response_model=List[PackageOut], summary="List all active packages")
def list_packages(db: Session = Depends(get_db)):
    return package_service.get_all(db)


@router.get("/{package_id}", response_model=PackageOut, summary="Get a single package")
def get_package(package_id: int, db: Session = Depends(get_db)):
    package = package_service.get_by_id(db, package_id)
    if not package:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Package not found")
    return package


@router.post(
    "/",
    response_model=PackageOut,
    status_code=status.HTTP_201_CREATED,
    summary="Create a package with features",
)
def create_package(payload: PackageCreate, db: Session = Depends(get_db)):
    if package_service.get_by_slug(db, payload.slug):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Package with slug '{payload.slug}' already exists",
        )
    return package_service.create(db, payload)
