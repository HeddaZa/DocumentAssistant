from pydantic import BaseModel


class TestResult(BaseModel):
    """Represents the result of a medical test."""

    test_name: str
    value: str
    unit: str | None
    reference_range: str | None
    date: str | None
    notes: str | None


class ResultExtraction(BaseModel):
    """Represents the extraction of medical test results for a patient."""

    patient_name: str | None
    test_results: list[TestResult]
    overall_notes: str | None
