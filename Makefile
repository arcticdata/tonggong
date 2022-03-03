install:
	pipenv sync --dev
	pipenv clean

fmt:
	pipenv run black .

lint:
	pipenv run black --check .

test:
	pipenv run pytest
