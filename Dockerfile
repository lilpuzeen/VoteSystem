ARG PYTHON_VERSION=3.10
FROM python:${PYTHON_VERSION}-slim as base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/fastapi_app/src

WORKDIR /fastapi_app
COPY . .

RUN pip install poetry \
    && poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

EXPOSE 8000

#CMD ["gunicorn", "src.main:app", "--bind=0.0.0.0:8000"]
