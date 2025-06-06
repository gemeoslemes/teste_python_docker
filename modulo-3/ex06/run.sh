#!/bin/bash

# Criar uma rede Docker personalizada
docker network create app_network || true

# Subir o banco de dados PostgreSQL
docker run -d \
    --name postgres_db \
    --network app_network \
    -e POSTGRES_USER=postgres \
    -e POSTGRES_PASSWORD=minhasenha \
    -e POSTGRES_DB=ningipoints \
    -p 5432:5432 \
    postgres:latest

# Construir e subir a aplicação FastAPI
docker build -t fastapi_app .
docker run -d \
    --name fastapi_container \
    --network app_network \
    -p 8080:8080 \
    fastapi_app
