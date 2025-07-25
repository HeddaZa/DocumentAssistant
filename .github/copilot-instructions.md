# GitHub Copilot Instruction File

## Coding Standards
- All code must be compliant with [ruff](https://docs.astral.sh/ruff/) (Python linter and formatter).
- All code must be type-checked and compliant with [mypy](http://mypy-lang.org/) (static type checker for Python).
- Docstrings for public methods should be single-line unless otherwise specified.
- Use modern Python syntax (e.g., type hints, | for unions).
- Follow project-specific conventions as seen in the codebase.

## Best Practices
- Prefer explicit imports and avoid wildcard imports.
- Use descriptive variable and function names.
- Add logging where appropriate, following the project's logger setup.
- Avoid code repetition; use comments like `# ...existing code...` when showing partial edits.

## Formatting
- Ensure code is formatted according to ruff's rules before submitting.
- Run mypy and ruff locally before pushing changes.

## Example Compliance
- See `documentassistent/agents/note_agent.py` for docstring and method style.
- See `documentassistent/structure/pydantic_llm_calls/` for type hinting and model style.

---
This file is intended for all contributors and for GitHub Copilot to ensure code quality and consistency.
