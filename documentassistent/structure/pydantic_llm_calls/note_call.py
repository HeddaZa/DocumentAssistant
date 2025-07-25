from pydantic import BaseModel


class NoteExtraction(BaseModel):
    """Model for extracting note information."""

    author: str | None
    date: str | None
    content: str
    tags: list[str] | None
