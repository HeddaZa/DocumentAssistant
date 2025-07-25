from documentassistent.structure.state import State


def test_state_initialization() -> None:
    state = State(prompt="Test", text="Some text")
    assert state.prompt == "Test"
    assert state.text == "Some text"
