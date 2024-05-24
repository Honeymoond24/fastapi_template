FROM python:3.12.0-slim-bookworm

RUN apt-get update && \
    apt-get install -y gcc libpq-dev && \
    apt clean && \
    rm -rf /var/cache/apt/*
ENV PYTHONPATH=/app/src

WORKDIR /app

COPY . .
RUN pip install -e .

COPY src /app/src

CMD ["alembic", "upgrade", "head"]
