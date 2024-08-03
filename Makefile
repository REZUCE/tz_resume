run:
	poetry run uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload --env-file ${ENV}

migrate-create:
	alembic revision --autogenerate -m ${MIGRATION}

migrate-apply:
	alembic upgrade head