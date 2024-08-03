FROM python:3.11-slim

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN pip install --upgrade pip && pip install poetry==1.8.3

WORKDIR /app/workers

COPY pyproject.toml poetry.lock ./

RUN touch README.md

RUN poetry install --without dev && rm -rf $POETRY_CACHE_DIR

COPY . .

RUN poetry install --without dev

# Run Alembic migrations

CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]