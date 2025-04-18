.PHONY: all test run lint clean

### Default target(s)
all: test

### Perform static analysis
lint:
	uv run ruff check --select I --fix .
	uv run ruff format .
	uv run ruff check . --fix

### Run the project
run: lint
	uv run rest-box

### Run unit tests
test: lint
	uv run pytest -s -vv

### Clean up generated files
clean:
	uv clean
	rm -fr .ruff_cache .venv

### Install this tool locally
install:
	uv tool install --upgrade .
