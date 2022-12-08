FROM postgres:latest
COPY initsql.sql /docker-entrypoint-initdb.d/
WORKDIR /usr/src/
COPY . /usr/src/
