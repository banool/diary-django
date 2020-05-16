# Build everything in the first stage
FROM python:3.8-alpine as base

FROM base as builder

WORKDIR /install

COPY requirements.txt /install

# Build MySQL library
RUN apk update
RUN apk add gcc python3-dev musl-dev mariadb-connector-c-dev mysql-client

RUN pip install --install-option="--prefix=/install" -r requirements.txt

# Real image
FROM base

WORKDIR /container

# Copy in build from previous stage
COPY --from=builder /install /usr/local
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
USER root
EXPOSE 11112
RUN apk add nginx openrc
RUN sed -i 's@return 404\;@@' /etc/nginx/conf.d/default.conf
RUN sed -i 's@# Everything.*@root /container/static;@' /etc/nginx/conf.d/default.conf
RUN sed -i 's@80@11112@g' /etc/nginx/conf.d/default.conf
RUN rc-update add nginx default

# Run server
ENV INTERNAL_PORT 11111

EXPOSE $INTERNAL_PORT
ENTRYPOINT /container/run.sh $INTERNAL_PORT
