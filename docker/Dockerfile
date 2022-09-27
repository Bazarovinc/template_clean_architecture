FROM python:3.10-alpine

ARG POETRY_PARAMS=""
ENV PYTHONUNBUFFERED 1
ENV POETRY_VIRTUALENVS_CREATE=false
ENV PATH="${PATH}:/root/.local/bin"

RUN mkdir /app
WORKDIR /app/
COPY /docker/wait-for /usr/bin/
RUN chmod +x /usr/bin/wait-for
RUN apk add --no-cache libpq libffi librdkafka
COPY pyproject.toml poetry.lock /app/
RUN apk add --no-cache \
    git `# для установки зависимостей из git` \
    libpq `# для psycopg2` \
    openssl openssl-dev
RUN apk add --no-cache --virtual build-deps \
    git `# для установки зависимостей из git` \
    make gcc g++ `# для сборки пакетов` \
    postgresql-dev `# для psycopg2` \
    librdkafka-dev `# для работы confluent-kafka` \
    libffi-dev `# для ffi` \
    && pip install --upgrade pip \
    && pip install poetry \
    && poetry install $POETRY_PARAMS --no-interaction --no-ansi \
    && apk del --no-cache build-deps
COPY / /app/
RUN chmod +x /app/docker/entrypoint.sh
