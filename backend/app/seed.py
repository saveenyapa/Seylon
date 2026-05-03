"""
Seed the database with initial vehicles and packages.
Run once after first launch:
    python -m app.seed
The seed is idempotent — it will not insert duplicate rows.
"""
import sys
import os

# Ensure the project root is on sys.path when run directly
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app.database import SessionLocal, engine, Base
from app.models import Vehicle, Package, PackageFeature  # registers models with Base

VEHICLES = [
    dict(name="Mercedes-Benz S-Class",   sub="Luxury Saloon · 2024",  tag="luxury",      price=60000,
         image_url="https://images.unsplash.com/photo-1618843479313-40f8afb4b4d8?auto=format&fit=crop&w=900&q=80"),
    dict(name="BMW 7 Series",             sub="Executive Saloon · 2023", tag="luxury",    price=55000,
         image_url="https://images.unsplash.com/photo-1555215695-3004980ad54e?auto=format&fit=crop&w=900&q=80"),
    dict(name="Land Rover Defender",      sub="Premium SUV · 2024",    tag="suv",         price=65000,
         image_url="https://images.unsplash.com/photo-1606664515524-ed2f786a0bd6?auto=format&fit=crop&w=900&q=80"),
    dict(name="Rolls-Royce Silver Shadow",sub="Vintage · 1972",        tag="vintage",     price=140000,
         image_url="https://images.unsplash.com/photo-1583121274602-3e2820c69888?auto=format&fit=crop&w=900&q=80"),
    dict(name="Range Rover Vogue",        sub="Premium SUV · 2023",    tag="suv",         price=75000,
         image_url="https://images.unsplash.com/photo-1519440317898-a4d3fb6e286f?auto=format&fit=crop&w=900&q=80"),
    dict(name="Mercedes-Benz E-Class",    sub="Convertible · 2022",    tag="convertible", price=50000,
         image_url="https://images.unsplash.com/photo-1494976388531-d1058494cdd8?auto=format&fit=crop&w=900&q=80"),
    dict(name="Audi A8 L",               sub="Luxury Saloon · 2024",  tag="luxury",      price=58000,
         image_url="https://images.unsplash.com/photo-1503376780353-7e6692767b70?auto=format&fit=crop&w=900&q=80"),
    dict(name="Jaguar Mark II",           sub="Vintage · 1968",        tag="vintage",     price=130000,
         image_url="https://images.unsplash.com/photo-1525609004556-c46c7d6cf023?auto=format&fit=crop&w=900&q=80"),
    dict(name="BMW M850i",               sub="Convertible · 2024",    tag="convertible", price=80000,
         image_url="https://images.unsplash.com/photo-1549399542-7e3f8b79c341?auto=format&fit=crop&w=900&q=80"),
]

PACKAGES = [
    dict(
        name="The Vow", slug="the-vow", hours=2,
        description="Ceremony to reception. The classic short-haul fairytale.",
        price=30000, is_featured=False,
        features=[
            dict(text="Tuxedoed chauffeur",          included=True,  sort_order=1),
            dict(text="Standard floral dressing",    included=True,  sort_order=2),
            dict(text="Chilled water & refreshments",included=True,  sort_order=3),
            dict(text="Photo-stop coordination",     included=False, sort_order=4),
            dict(text="Backup secondary vehicle",    included=False, sort_order=5),
        ],
    ),
    dict(
        name="The Garland", slug="the-garland", hours=4,
        description="Pre-ceremony portraits, ceremony, scenic drive, reception entry.",
        price=60000, is_featured=True,
        features=[
            dict(text="Tuxedoed chauffeur",                  included=True,  sort_order=1),
            dict(text="Premium floral or greenery dressing", included=True,  sort_order=2),
            dict(text="Sparkling on ice in cabin",           included=True,  sort_order=3),
            dict(text="Photo-stop coordination",             included=True,  sort_order=4),
            dict(text="Backup secondary vehicle",            included=False, sort_order=5),
        ],
    ),
    dict(
        name="The Diamond", slug="the-diamond", hours=12,
        description="Full day, every detail. From morning robes to last dance.",
        price=120000, is_featured=False,
        features=[
            dict(text="Two tuxedoed chauffeurs",    included=True, sort_order=1),
            dict(text="Bespoke imported florals",   included=True, sort_order=2),
            dict(text="Sparkling on ice + canapés", included=True, sort_order=3),
            dict(text="Photo-stop coordination",    included=True, sort_order=4),
            dict(text="Backup secondary vehicle",   included=True, sort_order=5),
        ],
    ),
]


def seed():
    print("Creating tables …")
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        # ── Vehicles ─────────────────────────────────────────────────────────
        existing_vehicles = db.query(Vehicle).count()
        if existing_vehicles == 0:
            for v in VEHICLES:
                db.add(Vehicle(**v))
            db.commit()
            print(f"  ✓ Inserted {len(VEHICLES)} vehicles")
        else:
            print(f"  · Vehicles already seeded ({existing_vehicles} rows) — skipping")

        # ── Packages ─────────────────────────────────────────────────────────
        existing_packages = db.query(Package).count()
        if existing_packages == 0:
            for p in PACKAGES:
                features = p.pop("features")
                pkg = Package(**p)
                for f in features:
                    pkg.features.append(PackageFeature(**f))
                db.add(pkg)
            db.commit()
            print(f"  ✓ Inserted {len(PACKAGES)} packages with features")
        else:
            print(f"  · Packages already seeded ({existing_packages} rows) — skipping")

    finally:
        db.close()

    print("Seed complete.")


if __name__ == "__main__":
    seed()
