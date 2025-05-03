from pydantic import BaseModel


class State(BaseModel):
    """Pydantic model for representing the state with a prompt, input text, and result."""

    prompt: str
    text: str
    result: str | None = None
