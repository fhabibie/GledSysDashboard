FROM python:3.10-slim-bullseye

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get -y install \
    # geodjango
    gdal-bin binutils libproj-dev libgdal-dev python3-gdal\
    # postgresql
    libpq-dev postgresql-client && \
    apt-get clean all && rm -rf /var/apt/lists/* && rm -rf /var/cache/apt/*

COPY requirements.txt /app/
RUN pip install -r requirements.txt
COPY . /app/