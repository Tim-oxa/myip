FROM python:3.14-slim AS builder

WORKDIR /app

RUN pip install --no-cache-dir uv

COPY pyproject.toml ./

RUN uv sync --no-dev

FROM python:3.14-slim

WORKDIR /app

COPY --from=builder /usr/local /usr/local

COPY . .

CMD ["python", "main.py"]
