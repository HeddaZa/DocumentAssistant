"""File management utilities for document storage."""

import hashlib
import shutil
from pathlib import Path

from documentassistent.utils.logger import setup_logger

logger = setup_logger(
    name="FileManager",
    log_file="logs/file_manager.log",
)


def compute_file_hash(file_path: str) -> str:
    """Compute SHA256 hash of a file."""
    sha256_hash = hashlib.sha256()
    with Path(file_path).open("rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()


def get_file_size(file_path: str) -> int:
    """Get file size in bytes."""
    return Path(file_path).stat().st_size


def sanitize_filename(text: str, max_length: int = 50) -> str:
    """Sanitize text for use in filename."""
    invalid_chars = '<>:"/\\|?*'
    sanitized = "".join(c if c not in invalid_chars else "_" for c in text)
    sanitized = sanitized.strip().replace(" ", "_")
    if len(sanitized) > max_length:
        sanitized = sanitized[:max_length]
    return sanitized or "unnamed"


def rename_file_with_id(
    original_path: str,
    document_id: int,
    doc_type: str,
    date: str,
    file_hash: str,
) -> str:
    """Rename file following pattern: {id}_{type}_{date}_{hash}.ext."""
    path = Path(original_path)
    extension = path.suffix
    short_hash = file_hash[:8]
    sanitized_date = sanitize_filename(date, max_length=10)
    sanitized_type = sanitize_filename(doc_type, max_length=15)

    new_filename = (
        f"doc_{document_id}_{sanitized_type}_{sanitized_date}_{short_hash}{extension}"
    )
    new_path = path.parent / new_filename

    try:
        shutil.move(str(path), str(new_path))
        logger.info(
            "File renamed",
            extra={
                "original": str(path),
                "new": str(new_path),
                "document_id": document_id,
            },
        )
        return str(new_path)
    except Exception:
        logger.exception(
            "Failed to rename file",
            extra={"document_id": document_id},
        )
        raise
