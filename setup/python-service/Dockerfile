FROM python:3.11.6-slim-bookworm

ARG PROJECT_PATH
WORKDIR $PROJECT_PATH

RUN set -eux; \
    python3.11 -m venv ./.venv; \
    ./.venv/bin/pip install -U pip setuptools; \
    ./.venv/bin/pip install poetry
