FROM python:3.9-alpine


ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
RUN apk add --update --no-cache jpeg-dev mariadb-dev RUN netcat-openbsd
RUN apk add --update --no-cache --virtual .tmp-build-deps \
      gcc libc-dev linux-headers python3-dev \
      musl-dev zlib zlib-dev
RUN pip install -r /requirements.txt
RUN apk del .tmp-build-deps

RUN mkdir /app
WORKDIR /app
COPY ./app /app

RUN mkdir -p /data/web/media
RUN mkdir -p /data/web/static
RUN adduser -D user
RUN chown -R user:user /data/
RUN chmod -R 755 /data/web
RUN chmod -R 755 ./run.sh
USER user
