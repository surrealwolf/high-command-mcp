.PHONY: help install dev test lint format clean docker-build docker-run docs run

help:
	@echo "High-Command - Helldivers 2 MCP Server"
	@echo ""
	@echo "Available targets:"
	@echo "  install        Install dependencies"
	@echo "  dev            Install development dependencies"
	@echo "  run            Run the MCP server"
	@echo "  test           Run tests with coverage"
	@echo "  test-fast      Run tests without coverage"
	@echo "  lint           Run linters (ruff, mypy)"
	@echo "  format         Format code with black and ruff"
	@echo "  clean          Remove build artifacts and cache files"
	@echo "  docker-build   Build Docker image"
	@echo "  docker-run     Run Docker container"
	@echo "  docs           Build documentation"
	@echo "  docs-serve     Serve documentation locally"
	@echo "  help           Show this help message"

install:
	pip install -e .

dev:
	pip install -e ".[dev]"

run:
	python -m highcommand.server

test:
	pytest

test-fast:
	pytest --no-cov -q

lint:
	ruff check .
	mypy mcp --ignore-missing-imports

format:
	black mcp tests scripts
	ruff check --fix .

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf build dist .pytest_cache .mypy_cache htmlcov .ruff_cache

docker-build:
	docker build -t high-command:latest .

docker-run: docker-build
	docker run -it --rm \
		-e HD_API_KEY=${HD_API_KEY} \
		-e X_SUPER_CLIENT=hc.dataknife.ai \
		-e X_SUPER_CONTACT=lee@fullmetal.dev \
		high-command:latest

docs:
	cd docs && make html

docs-serve: docs
	@echo "Serving docs at http://localhost:8000"
	python -m http.server 8000 -d docs/_build/html

check: lint test

all: clean install lint test
