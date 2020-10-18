FROM python:3.7-alpine3.8 as prod
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements/prod.txt requirements/prod.txt
RUN apk update \
# install psycopg2 dependencies
    && apk add --no-cache postgresql-libs \
        zlib-dev \
        jpeg-dev \
    && apk add --no-cache --virtual .requirements-build-deps \
        gcc \
        musl-dev \
        postgresql-dev \
        libffi-dev \
        libxml2-dev \
        libxslt-dev \
# install requirements
    && pip install --no-cache-dir -r requirements/prod.txt \
    && rm -r requirements \
    && apk del .requirements-build-deps

COPY . .

EXPOSE 5000
ENTRYPOINT [ "/app/scripts/entrypoint.sh" ]
CMD [ "/usr/local/bin/honcho", "-f", "/app/scripts/Procfile", "start" ]


FROM prod as dev
RUN pip install --no-cache-dir -r requirements/dev.txt
