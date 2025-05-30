from enum import Enum

from pydantic import BaseModel


class InvoiceTypeEnum(str, Enum):
    """Enum for representing the type of document."""

    DOCTOR_RECEIPT = "receipt_from_doctor"
    STATIONERY_RECEIPT = "receipt_for_stationery"
    FLAT_RECEIPT = "receipt_for_flat"
    OTHER = "other"


class Logs(BaseModel):
    """Pydantic model for representing a single log entry."""

    log: str
    date: str


class DocumentType(BaseModel):
    """Pydantic model for representing the type of document."""

    type: InvoiceTypeEnum
    price: float
    date: str
    description: str
    notes: str
    logs: list[Logs]
