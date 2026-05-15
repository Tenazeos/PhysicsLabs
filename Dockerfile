FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS builder

ENV UV_NO_DEV=1
ENV UV_LOCKED=1
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy
ENV UV_PYTHON_DOWNLOADS=0
ARG UV_CACHE_DIR=/cache/uv

WORKDIR /app

RUN --mount=type=cache,target=$UV_CACHE_DIR \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --no-install-project

COPY labs/ ./labs/
COPY main.py ./

RUN --mount=type=cache,target=$UV_CACHE_DIR \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync


FROM python:3.12-slim-bookworm

RUN groupadd --system app && useradd --system --gid app app

COPY --from=builder --chown=app:app /app /app
WORKDIR /app
ENV PATH="/app/.venv/bin:$PATH"

USER app

ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0
ENV STREAMLIT_SERVER_PORT=8501
CMD ["streamlit", "run", "main.py"]
EXPOSE $STREAMLIT_SERVER_PORT
