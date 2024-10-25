FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update \
    && apt-get install -y \
        libpq-dev \
        build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

RUN pip install psycopg2[pool]

COPY . .
COPY .env .env

CMD ["gunicorn --workers 3 --bind 0.0.0.0:8000 todo_proweb.wsgi:application"]
