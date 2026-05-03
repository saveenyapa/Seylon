import enum
from datetime import datetime, timezone
from sqlalchemy import Integer, String, Boolean, DateTime, ForeignKey, Text, Enum, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base


class EnquiryStatus(str, enum.Enum):
    PENDING   = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"


class Enquiry(Base):
    __tablename__ = "enquiries"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    # Customer details
    full_name: Mapped[str] = mapped_column(String(150), nullable=False)
    phone: Mapped[str] = mapped_column(String(30), nullable=False)

    # Event details
    wedding_date: Mapped[str] = mapped_column(String(10), nullable=False)    # ISO date "YYYY-MM-DD"
    vehicle_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("vehicles.id", ondelete="SET NULL"), nullable=True, index=True
    )
    pickup_time: Mapped[str] = mapped_column(String(5), nullable=False)      # "HH:MM"
    return_time: Mapped[str] = mapped_column(String(5), nullable=False)      # "HH:MM"
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Admin-managed
    status: Mapped[EnquiryStatus] = mapped_column(
        Enum(EnquiryStatus),
        default=EnquiryStatus.PENDING,
        nullable=False,
        index=True,
    )

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    # Relationship (optional eager load)
    vehicle: Mapped["Vehicle"] = relationship("Vehicle", lazy="joined")  # type: ignore[name-defined]

    def __repr__(self) -> str:
        return f"<Enquiry id={self.id} name={self.full_name!r} status={self.status}>"
