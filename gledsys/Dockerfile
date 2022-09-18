FROM python:3.10-slim-bullseye

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN echo "Installing Geospatial libs"
RUN apt-get update
RUN apt-get -y install gdal-bin binutils libproj-dev libgdal-dev python3-gdal g++

RUN echo "Installing postgre client libs"
RUN apt-get -y install libpq-dev postgresql-client

# Build GMT
# https://github.com/GenericMappingTools/gmt/blob/master/BUILDING.md
RUN echo "Installing GMT dependencies"
RUN apt-get -y install git cmake netcdf-bin cdftools 
RUN apt-get -y install build-essential libcurl4-gnutls-dev libnetcdf-dev
RUN apt-get -y install gmt-gshhg-full gmt-dcw

RUN echo "Installing GMT optional dependencies"
RUN apt-get -y install libfftw3-dev libpcre3-dev liblapack-dev libblas-dev libglib2.0-dev ghostscript

RUN echo "Clone GMT repository"
RUN git clone --depth 50 https://github.com/GenericMappingTools/gmt

RUN echo "Build and install GMT"
RUN cd gmt && mkdir build && cd build && cmake .. && cmake --build . && cmake --build . --target install

RUN echo "Removing GMT SC"
RUN rm -rf gmt

RUN echo "Cleaning apt list"
RUN apt-get clean all && rm -rf /var/apt/lists/* && rm -rf /var/cache/apt/*

RUN echo "Installing Django, pygmt, geopands, etc"
COPY requirements.txt /app/
RUN pip install -r requirements.txt
COPY . /app/