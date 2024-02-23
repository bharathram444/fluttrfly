.PHONY: check lint test test-cov

check:
	poetry run black --check .
	poetry run ruff check .

lint:
	poetry run black .
	poetry run ruff --fix .

test:
	poetry run pytest

test-cov:
	poetry run pytest --cov=fluttrfly --cov-branch --cov-report=term:skip-covered --cov-report=html
	poetry run coverage xml