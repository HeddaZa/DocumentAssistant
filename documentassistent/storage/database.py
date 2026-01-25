"""Database connection and session management."""

from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from documentassistent.exceptions import DatabaseConnectionError
from documentassistent.storage.models import Base
from documentassistent.utils.logger import setup_logger

logger = setup_logger(
    name="DatabaseManager",
    log_file="logs/database.log",
)

_engine = None
_SessionLocal = None


def init_database(db_path: str) -> None:
    """Initialize the database connection and create tables."""
    global _engine, _SessionLocal  # noqa: PLW0603

    db_file = Path(db_path)
    db_file.parent.mkdir(parents=True, exist_ok=True)

    _engine = create_engine(
        f"sqlite:///{db_path}",
        echo=False,
        connect_args={"check_same_thread": False},
    )

    Base.metadata.create_all(bind=_engine)
    _SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=_engine)

    logger.info("Database initialized", extra={"db_path": db_path})


def get_session() -> Session:
    """Get a database session."""
    if _SessionLocal is None:
        msg = "Database not initialized. Call init_database() first."
        raise DatabaseConnectionError(msg)
    return _SessionLocal()
