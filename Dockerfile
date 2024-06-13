FROM python:3.12.0-slim-bookworm

RUN apt-get update && \
    apt-get install -y gcc libpq-dev && \
    apt clean && \
    rm -rf /var/cache/apt/*

WORKDIR /app

RUN mkdir ./src

COPY ./pyproject.toml .
RUN pip install uv
RUN uv pip install -e . --system

COPY . .
