# Build everything in the first stage
FROM python:3.8-alpine as base

FROM base as builder

WORKDIR /install

COPY requirements.txt /install

# Build MySQL library
RUN apk update
RUN apk add gcc python3-dev musl-dev mariadb-connector-c-dev mysql-client

RUN pip install --install-option="--prefix=/release" -r requirements.txt

# Real image
FROM base

USER root

WORKDIR /container

# Copy in build from previous stage
COPY --from=builder /release /usr/local
COPY . .

# Docker specific environment vars
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Install only the MySQL stuff we need
RUN apk update
RUN apk add mariadb-connector-c-dev

# Other stuff
ENV DJANGO_SETTINGS_MODULE diary.settings.settings_prod
RUN apk add git openssh

# Serve static content
EXPOSE 11112

# Run server
ENV INTERNAL_PORT 11111

EXPOSE $INTERNAL_PORT
ENTRYPOINT /container/run.sh $INTERNAL_PORT
