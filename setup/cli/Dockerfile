FROM python:3.11.6-slim-bookworm

ARG PROJECT_PATH
WORKDIR $PROJECT_PATH

RUN set -eux; \
    apt-get update; \
    apt-get -y install netcat-openbsd

RUN set -eux; \
    apt-get -y install postgresql

RUN set -eux; \
    apt-get -y install neovim; \
    apt-get -y install httpie

RUN set -eux; \
    python3.11 -m venv ./.venv; \
    ./.venv/bin/pip install -U pip setuptools; \
    ./.venv/bin/pip install poetry
