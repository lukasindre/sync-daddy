.PHONY: fix
fix:
	uv run ruff check . --fix
	uv run ruff format .

.PHONY: check
check:
	uv run ruff check .
	uv run ruff format . --check
	uv run mypy . --strict