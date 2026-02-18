install:
	poetry install

web:
	poetry run printclaw web

diagnose:
	poetry run printclaw diagnose --export json

test:
	poetry run pytest -q

lint:
	poetry run ruff check .
	poetry run black --check .
