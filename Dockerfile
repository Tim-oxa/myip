FROM ghcr.io/astral-sh/uv:python3.14-trixie-slim
WORKDIR /app

COPY pyproject.toml ./
RUN uv sync --no-dev

COPY . .

CMD ["uv", "run", "main.py"]
