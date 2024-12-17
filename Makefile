.PHONY: test format lint typecheck check
.DEFAULT_GOAL := all

test:
	pip install -e .
	pytest

format:
	black .
	isort .
	ruff check --fix .


lint:
	black --check .
	isort --check .
	ruff check .

typecheck:
	mypy src/mcp_shell_server tests

coverage:
	pytest --cov=src/mcp_shell_server tests

# Run all checks required before pushing
check:  lint typecheck test
fix: check format
all: check test coverage
