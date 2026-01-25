"""Repository for CRUD operations on document extractions."""

from dataclasses import dataclass

from documentassistent.storage.base_repository import BaseRepository
from documentassistent.storage.models import (
    Document,
    InvoiceExtraction,
    InvoiceLog,
    NoteExtraction,
    NoteTag,
    ResultExtraction,
    TestResult,
)
from documentassistent.structure.pydantic_llm_calls.classification_call import (
    Classification,
)
from documentassistent.structure.pydantic_llm_calls.invoice_call import (
    InvoiceExtraction as InvoiceExtractionPydantic,
)
from documentassistent.structure.pydantic_llm_calls.note_call import (
    NoteExtraction as NoteExtractionPydantic,
)
from documentassistent.structure.pydantic_llm_calls.result_call import (
    ResultExtraction as ResultExtractionPydantic,
)
from documentassistent.utils.logger import setup_logger

logger = setup_logger(
    name="DocumentRepository",
    log_file="logs/database.log",
)


@dataclass
class FileMetadata:
    """Metadata about a file being stored."""

    path: str
    hash: str
    size: int
    type: str


class DocumentRepository(BaseRepository[Document]):
    """Repository for managing document storage operations."""

    def __init__(self) -> None:
        """Initialize DocumentRepository."""
        super().__init__(Document)

    def save_document(
        self,
        file_metadata: FileMetadata,
        classification: Classification,
        text_content: str | None = None,
    ) -> int:
        """Save document metadata and return the document ID."""
        with self._session() as session:
            document = Document(
                original_path=file_metadata.path,
                file_hash=file_metadata.hash,
                file_size=file_metadata.size,
                file_type=file_metadata.type,
                classification_label=classification.label,
                classification_confidence_level=classification.confidence.level,
                classification_confidence_explanation=classification.confidence.explanation,
                text_content=text_content,
            )
            session.add(document)
            session.flush()
            session.refresh(document)
            doc_id: int = document.id  # type: ignore[assignment]
            logger.info(
                "Document saved",
                extra={
                    "document_id": doc_id,
                    "classification": classification.label.value,
                },
            )
            return doc_id

    def update_renamed_path(self, document_id: int, renamed_path: str) -> None:
        """Update the renamed path for a document."""
        updated = self.update_by_id(document_id, renamed_path=renamed_path)
        if updated:
            logger.info(
                "Document renamed path updated",
                extra={"document_id": document_id, "renamed_path": renamed_path},
            )

    def save_invoice_extraction(
        self,
        document_id: int,
        extraction: InvoiceExtractionPydantic,
    ) -> None:
        """Save invoice extraction data."""
        with self._session() as session:
            invoice = InvoiceExtraction(
                document_id=document_id,
                type=extraction.type,
                price=extraction.price,
                date=extraction.date,
                description=extraction.description,
                notes=extraction.notes,
            )
            session.add(invoice)
            session.flush()

            for log_entry in extraction.logs:
                log = InvoiceLog(
                    invoice_extraction_id=invoice.id,
                    log=log_entry.log,
                    date=log_entry.date,
                )
                session.add(log)

            logger.info(
                "Invoice extraction saved",
                extra={"document_id": document_id, "price": extraction.price},
            )

    def save_note_extraction(
        self,
        document_id: int,
        extraction: NoteExtractionPydantic,
    ) -> None:
        """Save note extraction data."""
        with self._session() as session:
            note = NoteExtraction(
                document_id=document_id,
                author=extraction.author,
                date=extraction.date,
                content=extraction.content,
            )
            session.add(note)
            session.flush()

            if extraction.tags:
                for tag_value in extraction.tags:
                    tag = NoteTag(
                        note_extraction_id=note.id,
                        tag=tag_value,
                    )
                    session.add(tag)

            logger.info("Note extraction saved", extra={"document_id": document_id})

    def save_result_extraction(
        self,
        document_id: int,
        extraction: ResultExtractionPydantic,
    ) -> None:
        """Save medical test result extraction data."""
        with self._session() as session:
            result = ResultExtraction(
                document_id=document_id,
                patient_name=extraction.patient_name,
                overall_notes=extraction.overall_notes,
            )
            session.add(result)
            session.flush()

            for test in extraction.test_results:
                test_result = TestResult(
                    result_extraction_id=result.id,
                    test_name=test.test_name,
                    value=test.value,
                    unit=test.unit,
                    reference_range=test.reference_range,
                    date=test.date,
                    notes=test.notes,
                )
                session.add(test_result)

            logger.info(
                "Result extraction saved",
                extra={
                    "document_id": document_id,
                    "test_count": len(extraction.test_results),
                },
            )

    def get_document_by_hash(self, file_hash: str) -> Document | None:
        """Retrieve a document by its file hash."""
        return self.get_by_field(file_hash=file_hash)

    def get_document_by_id(self, document_id: int) -> Document | None:
        """Retrieve a document by its ID."""
        return self.get_by_id(document_id)

    def list_documents(
        self,
        limit: int | None = None,
        offset: int = 0,
        classification_label: str | None = None,
    ) -> list[Document]:
        """List documents with optional filtering and pagination."""
        if classification_label:
            return self.list_by_field(
                limit=limit,
                offset=offset,
                classification_label=classification_label,
            )
        return self.list_all(limit=limit, offset=offset)

    def count_documents(self, classification_label: str | None = None) -> int:
        """Count total documents, optionally filtered by classification."""
        if classification_label:
            return self.count(classification_label=classification_label)
        return self.count()

    def delete_document(self, document_id: int) -> bool:
        """Delete a document and its related extractions. Returns True if deleted."""
        return self.delete_by_id(document_id)
