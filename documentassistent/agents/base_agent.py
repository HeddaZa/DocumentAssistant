"""Base agent class with shared initialization and validation logic."""

from collections.abc import Callable
from functools import wraps
from typing import Any, TypeVar, cast

from documentassistent.exceptions import StateValidationError
from documentassistent.llm.base_llm import BaseLLM
from documentassistent.llm.llm_factory import ConfigDict, LLMFactory
from documentassistent.structure.state import BaseWorkflowState
from load_config import load_config

CONFIG = load_config("config.yaml")

StateT = TypeVar("StateT", bound=BaseWorkflowState)


def validate_state(func: Callable) -> Callable:
    """Decorator to validate state before method execution."""

    @wraps(func)
    def wrapper(
        self: BaseAgent,
        state: BaseWorkflowState,
        *args: Any,
        **kwargs: Any,
    ) -> BaseWorkflowState:
        if state is None:
            msg = "state must not be None"
            self.logger.error(msg)
            raise StateValidationError(msg)
        return cast("BaseWorkflowState", func(self, state, *args, **kwargs))

    return wrapper


class BaseAgent:
    """Base class for all agents with common LLM initialization and validation."""

    def __init__(
        self,
        agent_name: str,
        logger: Any,
        llm: BaseLLM | None = None,
    ) -> None:
        """Initialize the agent with LLM configuration."""
        self.logger = logger
        self.llm: BaseLLM = llm if llm is not None else self._create_default_llm()
        self.logger.info(
            "{} initialized with LLM: {}",
            agent_name,
            type(self.llm).__name__,
        )

    def _create_default_llm(self) -> BaseLLM:
        """Create default LLM from configuration."""
        # Get provider from config, fallback to 'ollama' for backward compatibility
        provider = CONFIG.get("llm", {}).get("provider", "ollama")
        model = CONFIG.get("llm", {}).get(
            "model",
            CONFIG.get(provider, {}).get("model"),
        )

        config: ConfigDict = {
            "llm": {
                "type": provider,
                "model": model,
            },
        }
        return LLMFactory.create_llm(config)

    def _convert_state(
        self,
        state: BaseWorkflowState,
        target_state_class: type[StateT],
    ) -> StateT:
        """Convert state to target state class, preserving all fields."""
        if isinstance(state, target_state_class):
            return state
        return target_state_class(**state.model_dump())
