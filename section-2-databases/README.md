Overview

Tools:
* pgAdmin

Docker:
* docker build -t postgres-local .
* docker run -d --name postgres-local -e POSTGRES_PASSWORD=postgres -p 5432:5432 postgres-local
* docker container ls
* docker logs postgres-local
* docker container stop postgres-local
* docker container rm postgres-local
* docker rmi postgres-local