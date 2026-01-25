"""Base repository with common CRUD operations and session management."""

from collections.abc import Generator
from contextlib import contextmanager
from typing import Any, Generic, TypeVar

from documentassistent.exceptions import DatabaseError
from documentassistent.storage.database import get_session
from documentassistent.utils.logger import setup_logger

logger = setup_logger(name="BaseRepository", log_file="logs/database.log")

T = TypeVar("T")


class BaseRepository(Generic[T]):
    """Base repository providing common database operations."""

    def __init__(self, model_class: type[T]) -> None:
        """Initialize repository with model class."""
        self.model_class = model_class

    @contextmanager
    def _session(self) -> Generator[Any, None, None]:
        """Context manager for database sessions with automatic cleanup."""
        session = get_session()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            logger.exception("Database operation failed, rolling back")
            error_msg = f"Database operation failed: {e!s}"
            raise DatabaseError(error_msg) from e
        finally:
            session.close()

    @contextmanager
    def _session_read_only(self) -> Generator[Any, None, None]:
        """Context manager for read-only operations (no commit)."""
        session = get_session()
        try:
            yield session
        finally:
            session.close()

    def get_by_id(self, entity_id: int) -> T | None:
        """Retrieve entity by ID."""
        with self._session_read_only() as session:
            result: T | None = (
                session.query(self.model_class).filter_by(id=entity_id).first()
            )
            return result

    def get_by_field(self, **filters: Any) -> T | None:
        """Retrieve first entity matching filters."""
        with self._session_read_only() as session:
            result: T | None = (
                session.query(self.model_class).filter_by(**filters).first()
            )
            return result

    def list_all(self, limit: int | None = None, offset: int = 0) -> list[T]:
        """List all entities with optional pagination."""
        with self._session_read_only() as session:
            query = session.query(self.model_class).offset(offset)
            if limit:
                query = query.limit(limit)
            results: list[T] = query.all()
            return results

    def list_by_field(
        self,
        limit: int | None = None,
        offset: int = 0,
        **filters: Any,
    ) -> list[T]:
        """List entities matching filters with optional pagination."""
        with self._session_read_only() as session:
            query = session.query(self.model_class).filter_by(**filters).offset(offset)
            if limit:
                query = query.limit(limit)
            results: list[T] = query.all()
            return results

    def count(self, **filters: Any) -> int:
        """Count entities matching filters."""
        with self._session_read_only() as session:
            query = session.query(self.model_class)
            if filters:
                query = query.filter_by(**filters)
            count_result: int = query.count()
            return count_result

    def exists(self, **filters: Any) -> bool:
        """Check if entity exists matching filters."""
        return self.count(**filters) > 0

    def delete_by_id(self, entity_id: int) -> bool:
        """Delete entity by ID. Returns True if deleted, False if not found."""
        with self._session() as session:
            instance = session.query(self.model_class).filter_by(id=entity_id).first()
            if instance:
                session.delete(instance)
                logger.info(
                    "Deleted %s with id=%s",
                    self.model_class.__name__,
                    entity_id,
                )
                return True
            return False

    def create(self, **kwargs: Any) -> T:
        """Create new entity."""
        with self._session() as session:
            instance = self.model_class(**kwargs)
            session.add(instance)
            session.flush()
            session.refresh(instance)
            logger.info("Created %s with id=%s", self.model_class.__name__, instance.id)  # type: ignore[attr-defined]
            return instance

    def update_by_id(self, entity_id: int, **updates: Any) -> T | None:
        """Update entity by ID. Returns updated entity or None if not found."""
        with self._session() as session:
            instance = session.query(self.model_class).filter_by(id=entity_id).first()
            if instance:
                for key, value in updates.items():
                    setattr(instance, key, value)
                session.flush()
                session.refresh(instance)
                logger.info(
                    "Updated %s with id=%s",
                    self.model_class.__name__,
                    entity_id,
                )
                result: T = instance
                return result
            return None
