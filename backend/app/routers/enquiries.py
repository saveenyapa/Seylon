from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.enquiry import EnquiryStatus
from app.schemas.enquiry import (
    EnquiryCreate, EnquiryOut, EnquiryStatusUpdate, EnquiryListOut,
)
from app.services import enquiry_service

router = APIRouter(prefix="/enquiries", tags=["Enquiries"])


@router.post(
    "/",
    response_model=EnquiryOut,
    status_code=status.HTTP_201_CREATED,
    summary="Submit a wedding enquiry",
)
def create_enquiry(payload: EnquiryCreate, db: Session = Depends(get_db)):
    return enquiry_service.create(db, payload)


@router.get(
    "/",
    response_model=EnquiryListOut,
    summary="List all enquiries (admin)",
)
def list_enquiries(
    status_filter: Optional[EnquiryStatus] = Query(None, alias="status"),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
):
    total, items = enquiry_service.get_all(
        db, status=status_filter, skip=skip, limit=limit
    )
    return EnquiryListOut(total=total, items=items)


@router.get(
    "/{enquiry_id}",
    response_model=EnquiryOut,
    summary="Get a single enquiry",
)
def get_enquiry(enquiry_id: int, db: Session = Depends(get_db)):
    enquiry = enquiry_service.get_by_id(db, enquiry_id)
    if not enquiry:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Enquiry not found")
    return enquiry


@router.patch(
    "/{enquiry_id}/status",
    response_model=EnquiryOut,
    summary="Update enquiry status (admin)",
)
def update_status(
    enquiry_id: int,
    payload: EnquiryStatusUpdate,
    db: Session = Depends(get_db),
):
    enquiry = enquiry_service.update_status(db, enquiry_id, payload)
    if not enquiry:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Enquiry not found")
    return enquiry
