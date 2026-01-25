import os
from collections.abc import Callable
from functools import wraps
from typing import Any

from dotenv import load_dotenv
from langfuse.callback import CallbackHandler

load_dotenv()


class LangfuseHandler:
    """Handler for integrating Langfuse callback functionality into LLM chains."""

    def __init__(self) -> None:
        self.secret_key = os.getenv("LANGFUSE_SECRET_KEY")
        self.public_key = os.getenv("LANGFUSE_PUBLIC_KEY")
        self.host = os.getenv("LANGFUSE_HOST")
        self.handler = CallbackHandler(
            secret_key=self.secret_key,
            public_key=self.public_key,
            host=self.host,
        )

    def get_handler(self) -> CallbackHandler:
        """
        Returns the Langfuse CallbackHandler instance.

        Returns
        -------
        CallbackHandler
            The initialized Langfuse CallbackHandler.
        """
        return self.handler

    def trace(self) -> Callable[[Any], Any]:
        """Decorator to add Langfuse callback to LLM chain calls."""

        def decorator(func: Callable[[Any], Any]) -> Callable[[Any], Any]:
            @wraps(func)
            def wrapper(*args: Any, **kwargs: Any) -> Any:
                # Add Langfuse callback handler to config
                if "config" not in kwargs:
                    kwargs["config"] = {}
                if "callbacks" not in kwargs["config"]:
                    kwargs["config"]["callbacks"] = []
                kwargs["config"]["callbacks"].append(self.handler)

                return func(*args, **kwargs)

            return wrapper

        return decorator
