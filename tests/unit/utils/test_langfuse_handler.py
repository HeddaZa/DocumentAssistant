from langfuse.callback import CallbackHandler

from documentassistent.utils.langfuse_handler import LangfuseHandler

EXPECTED_RESULT = 3


def test_langfuse_handler_trace() -> None:
    handler = LangfuseHandler()
    assert hasattr(handler, "trace")
    assert isinstance(handler.get_handler(), CallbackHandler)

    # Test that the trace decorator wraps and returns the function result
    @handler.trace()
    def dummy(x: int) -> int:
        return x + 1

    assert dummy(2) == EXPECTED_RESULT
