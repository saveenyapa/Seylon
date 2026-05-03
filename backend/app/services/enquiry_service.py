from typing import Optional, List, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import select, func

from app.models.enquiry import Enquiry, EnquiryStatus
from app.schemas.enquiry import EnquiryCreate, EnquiryStatusUpdate


def create(db: Session, payload: EnquiryCreate) -> Enquiry:
    enquiry = Enquiry(**payload.model_dump())
    db.add(enquiry)
    db.commit()
    db.refresh(enquiry)
    return enquiry


def get_by_id(db: Session, enquiry_id: int) -> Optional[Enquiry]:
    return db.get(Enquiry, enquiry_id)


def get_all(
    db: Session,
    *,
    status: Optional[EnquiryStatus] = None,
    skip: int = 0,
    limit: int = 50,
) -> Tuple[int, List[Enquiry]]:
    """Return (total_count, paginated_items)."""
    stmt = select(Enquiry)
    if status:
        stmt = stmt.where(Enquiry.status == status)
    stmt = stmt.order_by(Enquiry.created_at.desc())

    total: int = db.scalar(
        select(func.count()).select_from(stmt.subquery())
    ) or 0
    items = list(db.scalars(stmt.offset(skip).limit(limit)).all())
    return total, items


def update_status(
    db: Session,
    enquiry_id: int,
    payload: EnquiryStatusUpdate,
) -> Optional[Enquiry]:
    enquiry = db.get(Enquiry, enquiry_id)
    if not enquiry:
        return None
    enquiry.status = payload.status
    db.commit()
    db.refresh(enquiry)
    return enquiry
