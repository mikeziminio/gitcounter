FROM python:3.11.6-slim-bookworm
ARG PROJECT_PATH
RUN mkdir -p $PROJECT_PATH
WORKDIR $PROJECT_PATH

RUN set -eux; \
    python3.11 -m venv ./.venv; \
    ./.venv/bin/pip install -U pip setuptools; \
    ./.venv/bin/pip install poetry

CMD ["/bin/bash", "-c", "source ./.venv/bin/activate && poetry install --no-root && exec bash"]