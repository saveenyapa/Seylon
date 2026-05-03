from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from app.config import get_settings

settings = get_settings()

# SQLite needs check_same_thread=False for FastAPI's thread-pool workers
connect_args = (
    {"check_same_thread": False}
    if settings.database_url.startswith("sqlite")
    else {}
)

engine = create_engine(
    settings.database_url,
    connect_args=connect_args,
    echo=settings.debug,       # log SQL when DEBUG=true
)

# Enable WAL mode and foreign key enforcement for SQLite
@event.listens_for(engine, "connect")
def _sqlite_pragmas(dbapi_conn, _connection_record):
    if settings.database_url.startswith("sqlite"):
        cursor = dbapi_conn.cursor()
        cursor.execute("PRAGMA journal_mode=WAL")
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()


SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
)


class Base(DeclarativeBase):
    """Shared declarative base for all ORM models."""
    pass


# ─── Dependency ──────────────────────────────────────────────────────────────

def get_db():
    """
    FastAPI dependency that yields a database session and guarantees
    the session is closed after the request — even on errors.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
