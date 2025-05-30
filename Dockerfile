FROM python:3.12-slim

WORKDIR /src

COPY pyproject.toml poetry.lock /src/

RUN pip install poetry
RUN poetry lock
RUN poetry install --no-root


COPY . /src


CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]