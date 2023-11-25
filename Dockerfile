# Build everything in first stage
FROM python:3.11-buster as builder

RUN pip install poetry==1.7.1

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /app

COPY pyproject.toml poetry.lock ./

# Build MySQL library
RUN apt-get update
RUN apt-get install -y python3-dev mariadb-client

# Requirements
RUN poetry install --without dev --no-root && rm -rf $POETRY_CACHE_DIR

# The runtime image, used to just run the code provided its virtual environment
FROM python:3.11-slim-buster as runtime

ENV VIRTUAL_ENV=/app/.venv PATH="/app/.venv/bin:$PATH"

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

COPY . /app

# Docker specific environment vars
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Install only the MySQL stuff we need
RUN apt update
RUN apt install -y mariadb-client

# Other stuff
ENV DJANGO_SETTINGS_MODULE diary.settings.settings_prod
RUN apt install -y git

# Serve static content
EXPOSE 11112

# Run server
USER root
ENV INTERNAL_PORT 11111
EXPOSE $INTERNAL_PORT
EXPOSE $INTERNAL_PORT
WORKDIR /app
ENTRYPOINT ./run.sh $INTERNAL_PORT
