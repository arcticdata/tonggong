install:
	pipenv sync --dev
	pipenv clean

fmt:
	pipenv run isort .
	pipenv run black .

lint:
	pipenv run isort --check .
	pipenv run black --check .

test:
	pipenv run pytest --cov=./
