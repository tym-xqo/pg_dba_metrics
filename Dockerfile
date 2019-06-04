FROM alpine:3.8

RUN apk add --no-cache python3 py3-psycopg2

COPY . /app
WORKDIR /app

RUN pip3 install --upgrade pip pipenv && pipenv install --system

CMD dba_metrics
