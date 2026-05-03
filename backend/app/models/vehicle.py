from datetime import datetime, timezone
from sqlalchemy import Integer, String, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base


class Vehicle(Base):
    __tablename__ = "vehicles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    sub: Mapped[str] = mapped_column(String(120), nullable=False)       # subtitle e.g. "Luxury Saloon · 2024"
    tag: Mapped[str] = mapped_column(String(30), nullable=False, index=True)  # luxury|vintage|suv|convertible
    price: Mapped[int] = mapped_column(Integer, nullable=False)          # price per 4-hour block (LKR)
    image_url: Mapped[str] = mapped_column(String(512), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    def __repr__(self) -> str:
        return f"<Vehicle id={self.id} name={self.name!r} tag={self.tag!r}>"
