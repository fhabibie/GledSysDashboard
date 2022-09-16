FROM python:3.10-slim-bullseye

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN echo "Installing Geospatial libs"
RUN apt-get update
RUN apt-get -y install gdal-bin binutils libproj-dev libgdal-dev python3-gdal g++

RUN echo "Installing postgre client libs"
RUN apt-get -y install libpq-dev postgresql-client

RUN echo "Cleaning apt list"
RUN apt-get clean all && rm -rf /var/apt/lists/* && rm -rf /var/cache/apt/*

COPY requirements.txt /app/
RUN pip install -r requirements.txt
COPY . /app/