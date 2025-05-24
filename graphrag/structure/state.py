from pydantic import BaseModel  # type: ignore[import-not-found]


class State(BaseModel):
    """Pydantic model for representing the state."""

    prompt: str
    text: str
    result: str | None = None
