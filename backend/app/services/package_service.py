from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models.package import Package, PackageFeature
from app.schemas.package import PackageCreate


def get_all(db: Session, *, active_only: bool = True) -> List[Package]:
    stmt = select(Package)
    if active_only:
        stmt = stmt.where(Package.is_active == True)
    stmt = stmt.order_by(Package.hours)
    return list(db.scalars(stmt).all())


def get_by_id(db: Session, package_id: int) -> Optional[Package]:
    return db.get(Package, package_id)


def get_by_slug(db: Session, slug: str) -> Optional[Package]:
    stmt = select(Package).where(Package.slug == slug)
    return db.scalars(stmt).first()


def create(db: Session, payload: PackageCreate) -> Package:
    feature_data = payload.model_dump(exclude={"features"})
    package = Package(**feature_data)

    for f in payload.features:
        package.features.append(
            PackageFeature(
                text=f.text,
                included=f.included,
                sort_order=f.sort_order,
            )
        )

    db.add(package)
    db.commit()
    db.refresh(package)
    return package
