"""Storage agent for persisting document extraction results."""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Any, cast

if TYPE_CHECKING:
    from collections.abc import Callable

    from documentassistent.structure.state import State

from documentassistent.storage.repository import DocumentRepository, FileMetadata
from documentassistent.structure.pydantic_llm_calls.classification_call import (
    DocumentType,
)
from documentassistent.utils.file_manager import (
    compute_file_hash,
    get_file_size,
    rename_file_with_id,
)
from documentassistent.utils.logger import setup_logger

logger = setup_logger(
    name="StorageAgent",
    log_file="logs/storage_agent.log",
)


class StorageAgent:
    """Agent for storing document extraction results to database."""

    def __init__(self) -> None:
        self.repository = DocumentRepository()
        logger.info("StorageAgent initialized")

    def _get_extraction_info(
        self,
        state: State,
        classification_label: DocumentType,
        document_id: int,
    ) -> tuple[str, str]:
        """Get date and type for filename from extraction result."""
        extraction_config = {
            DocumentType.INVOICE: {
                "attr": "invoice_extraction_result",
                "save_method": self.repository.save_invoice_extraction,
                "get_info": lambda e: (e.date, e.type.value),
                "default": ("unknown", "invoice"),
            },
            DocumentType.NOTE: {
                "attr": "note_extraction_result",
                "save_method": self.repository.save_note_extraction,
                "get_info": lambda e: (e.date or "unknown", "note"),
                "default": ("unknown", "note"),
            },
            DocumentType.RESULT: {
                "attr": "result_extraction_result",
                "save_method": self.repository.save_result_extraction,
                "get_info": lambda _: ("unknown", "result"),
                "default": ("unknown", "result"),
            },
        }

        config = extraction_config.get(classification_label)
        if not config:
            logger.warning(
                "Unknown classification label",
                extra={"label": classification_label},
            )
            return "unknown", "unknown"

        attr_name = cast("str", config["attr"])
        save_method = cast("Callable[[int, Any], None]", config["save_method"])
        get_info = cast("Callable[[Any], tuple[str, str]]", config["get_info"])
        default = cast("tuple[str, str]", config["default"])

        extraction = getattr(state, attr_name)
        if extraction:
            save_method(document_id, extraction)
            return get_info(extraction)

        logger.warning("No extraction result found", extra={"attr": attr_name})
        return default

    def store_results(self, state: State) -> State:
        """Store document and extraction results, rename file with document ID."""
        if not state.file_path:
            logger.warning("No file_path in state, skipping storage")
            return state

        if not state.classification_result:
            logger.warning("No classification_result in state, skipping storage")
            return state

        file_path = state.file_path
        file_hash = compute_file_hash(file_path)
        file_size = get_file_size(file_path)
        file_type = Path(file_path).suffix.lower().lstrip(".")

        existing_doc = self.repository.get_document_by_hash(file_hash)
        if existing_doc:
            logger.info(
                "Document already exists",
                extra={
                    "document_id": existing_doc.id,
                    "file_path": file_path,
                },
            )
            return state.model_copy(update={"document_id": existing_doc.id})

        file_metadata = FileMetadata(
            path=file_path,
            hash=file_hash,
            size=file_size,
            type=file_type,
        )

        document_id = self.repository.save_document(
            file_metadata=file_metadata,
            classification=state.classification_result,
            text_content=state.text,
        )

        date_for_filename, type_for_filename = self._get_extraction_info(
            state,
            state.classification_result.label,
            document_id,
        )

        try:
            renamed_path = rename_file_with_id(
                original_path=file_path,
                document_id=document_id,
                doc_type=type_for_filename,
                date=date_for_filename,
                file_hash=file_hash,
            )
            self.repository.update_renamed_path(document_id, renamed_path)

            logger.success(
                "Document stored and renamed",
                extra={
                    "document_id": document_id,
                    "renamed_path": renamed_path,
                },
            )
        except OSError:
            logger.exception(
                "Failed to rename file, document saved but path not updated",
                extra={"document_id": document_id},
            )

        return state.model_copy(update={"document_id": document_id})
