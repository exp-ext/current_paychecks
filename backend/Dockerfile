FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml poetry.lock ./

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PIPENV_VENV_IN_PROJECT=1

RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-root --no-dev

COPY . .

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
