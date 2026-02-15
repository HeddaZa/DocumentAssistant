"""SQLAlchemy ORM models for document extractions."""

from datetime import datetime

from sqlalchemy import Column, DateTime, Enum, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import DeclarativeBase, relationship

from documentassistent.structure.pydantic_llm_calls.classification_call import (
    DocumentType,
)
from documentassistent.structure.pydantic_llm_calls.confidence import ConfidenceLevel
from documentassistent.structure.pydantic_llm_calls.invoice_call import (
    InvoiceTypeEnum,
)


class Base(DeclarativeBase):
    """Base class for all ORM models."""


class Document(Base):
    """Represents a processed document with metadata."""

    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, autoincrement=True)
    original_path = Column(String, nullable=False)
    renamed_path = Column(String, nullable=True)
    file_hash = Column(String(64), unique=True, nullable=False)
    file_size = Column(Integer, nullable=False)
    file_type = Column(String, nullable=False)
    classification_label: Column[DocumentType] = Column(
        Enum(DocumentType),
        nullable=False,
    )
    classification_confidence_level: Column[ConfidenceLevel] = Column(
        Enum(ConfidenceLevel),
        nullable=False,
    )
    classification_confidence_explanation = Column(Text, nullable=True)
    text_content = Column(Text, nullable=True)
    processed_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    invoice_extraction = relationship(
        "InvoiceExtraction",
        back_populates="document",
        uselist=False,
    )
    note_extraction = relationship(
        "NoteExtraction",
        back_populates="document",
        uselist=False,
    )
    result_extraction = relationship(
        "ResultExtraction",
        back_populates="document",
        uselist=False,
    )


class InvoiceExtraction(Base):
    """Represents extracted invoice information."""

    __tablename__ = "invoice_extractions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    document_id = Column(Integer, ForeignKey("documents.id"), nullable=False)
    type: Column[InvoiceTypeEnum] = Column(Enum(InvoiceTypeEnum), nullable=False)
    price = Column(Float, nullable=False)
    date = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    notes = Column(Text, nullable=True)

    document = relationship("Document", back_populates="invoice_extraction")
    logs = relationship("InvoiceLog", back_populates="invoice_extraction")


class InvoiceLog(Base):
    """Represents a log entry for an invoice."""

    __tablename__ = "invoice_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    invoice_extraction_id = Column(
        Integer,
        ForeignKey("invoice_extractions.id"),
        nullable=False,
    )
    log = Column(Text, nullable=False)
    date = Column(String, nullable=False)

    invoice_extraction = relationship("InvoiceExtraction", back_populates="logs")


class NoteExtraction(Base):
    """Represents extracted note information."""

    __tablename__ = "note_extractions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    document_id = Column(Integer, ForeignKey("documents.id"), nullable=False)
    author = Column(String, nullable=True)
    date = Column(String, nullable=True)
    content = Column(Text, nullable=False)

    document = relationship("Document", back_populates="note_extraction")
    tags = relationship("NoteTag", back_populates="note_extraction")


class NoteTag(Base):
    """Represents a tag for a note."""

    __tablename__ = "note_tags"

    id = Column(Integer, primary_key=True, autoincrement=True)
    note_extraction_id = Column(
        Integer,
        ForeignKey("note_extractions.id"),
        nullable=False,
    )
    tag = Column(String, nullable=False)

    note_extraction = relationship("NoteExtraction", back_populates="tags")


class ResultExtraction(Base):
    """Represents extracted medical test result information."""

    __tablename__ = "result_extractions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    document_id = Column(Integer, ForeignKey("documents.id"), nullable=False)
    patient_name = Column(String, nullable=True)
    overall_notes = Column(Text, nullable=True)

    document = relationship("Document", back_populates="result_extraction")
    test_results = relationship("TestResult", back_populates="result_extraction")


class TestResult(Base):
    """Represents a single medical test result."""

    __tablename__ = "test_results"

    id = Column(Integer, primary_key=True, autoincrement=True)
    result_extraction_id = Column(
        Integer,
        ForeignKey("result_extractions.id"),
        nullable=False,
    )
    test_name = Column(String, nullable=False)
    value = Column(String, nullable=False)
    unit = Column(String, nullable=True)
    reference_range = Column(String, nullable=True)
    date = Column(String, nullable=True)
    notes = Column(Text, nullable=True)

    result_extraction = relationship("ResultExtraction", back_populates="test_results")
