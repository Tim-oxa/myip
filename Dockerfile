FROM python:3.14-slim AS builder

WORKDIR /app

RUN wget -qO- https://astral.sh/uv/install.sh | sh

COPY pyproject.toml ./

RUN uv sync --no-dev

FROM python:3.14-slim

WORKDIR /app

COPY --from=builder /usr/local /usr/local

COPY . .

CMD ["uv", "run", "main.py"]
