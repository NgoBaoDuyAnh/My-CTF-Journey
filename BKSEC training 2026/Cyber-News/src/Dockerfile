FROM python:3.11.3-slim

WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

COPY pyproject.toml ./

RUN uv lock && uv sync --no-dev

COPY src/ ./src/
COPY templates/ ./src/templates/
COPY static/ ./src/static/

RUN mkdir -p /tmp && chmod 777 /tmp

WORKDIR /app/src

EXPOSE 8888

CMD ["uv", "run", "python", "app.py"]
