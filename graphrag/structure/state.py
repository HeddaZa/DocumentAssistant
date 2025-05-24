from pydantic import BaseModel


class State(BaseModel):
    """Pydantic model for representing the state."""

    prompt: str
    text: str
    result: str | None = None
