FROM python:3.12.4-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update  
RUN apt-get install -y python3-dev gcc libc-dev libffi-dev libpq-dev

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY ./src ./src

WORKDIR /app/src