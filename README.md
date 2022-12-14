# GledSys
![GledSys](docs/img/logo.png)
> GledSys, a GIS web platform that build with [GeoDjango](https://docs.djangoproject.com/en/4.1/ref/contrib/gis/) and [PostgreSQL](https://www.postgresql.org/) with [PostGIS](https://postgis.net/) extension

## Preview
![Preview](docs/img//thumbnail.jpg)
## Table of Contents
1. [Prerequisities](#prerequisities)
2. [Installation](#installation)
3. [Manual Installation](#manual-installation)
4. [Usage](#usage)

## Prerequisities
This project was built with Django and PostGIS database and developed under Docker Container. In order to run this project, you'll need the following dependecies:
- [Docker and Docker Compose](https://docs.docker.com/compose/install/)
- [Python and Pip](https://www.python.org/)
- [Geospatial Libraries (for manual installation)](https://docs.djangoproject.com/en/4.1/ref/contrib/gis/install/geolibs/)



## Installation
This instructions will cover basic installaion using `docker-compose`

### Install Docker and Docker Compose
Download docker and docker compose from the official [Docker Website](https://www.docker.com/). You can install Docker Desktop that provide both of docker and docker-compose.


### Clone Project
Clone the GledSys repository
```
git clone https://github.com/fhabibie/GledSysDashboard.git
```

or you can download the ZIP file project
```
wget https://github.com/fhabibie/GledSysDashboard/archive/refs/heads/main.zip
```

### Docker Compose Configuration
Open ```docker-compose.yml``` from the project directory. You can configure the database setting, such as password, username, and database name.
```
...
db:
    image: "postgis/postgis"
    restart: always 
    volumes:
      - ./data/db:/var/lib/postgresql/data
    environment:
      - POSTGRES_DB=postgres
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres
...

web:
    build:
      context: ./gledsys
    command: python manage.py runserver 0.0.0.0:8000
    restart: always
    volumes:
      - ./gledsys:/app
    ports:
      - "8000:8000"
    environment:
      - POSTGRES_NAME=postgres
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres
...

```

### Build docker container
Open your terminal / command line and build the docker container using following command:

```
docker-compose build 
```

This process will downloading PostGIS image, python and geospatial dependencies


### Run docker container
To run your docker container project, enter the following command

``` 
docker-compose up 
```

Show your running container using

``` 
docker-compose ps 
```

For more docker-compose commands, please read the following [documentations](https://docs.docker.com/compose/reference/)


### Migrating the database
``` 
# Makemigration
docker-compose exec web python manage.py makemigrations

# Migrate the database
docker-compose exec web python manage.py migrate
```

Create superuser for django admin

```
docker-compose exec web python manage.py createsuperuser
```


### Django and PostGIS Port
| Service       | Url / Port                   |
|---------------|------------------------------|
| Django        | http://localhost:8000/       |
| Django Admin  | http://localhost:8000/admin  |
| PostGIS       | 5432                         |

### Stop docker container
To stop your docker container, hit ```Ctrl-C``` or enter the following command
```
docker-compose down --volumes
```
You can also stop the container through Docker Desktop interface



### Cleaning the docker
Sometimes the docker will create some unused container/image and it take a lot of disk allocation. To clean up the docker container, just hit the following command
```
docker system prune
```



## Manual Installation
### Install Geospatial Libraries
You need to install GEOS, PROJ, GDAL, and GMT Spatial libraries. Follow external links to install these libraries.
* [GEOS](http://libgeos.org/usage/download/)
* [PROJ](https://proj.org/install.html)
* [GDAL/OGR](https://gdal.org/download.html)
* [GMT](https://www.generic-mapping-tools.org/download/)


### Install PostgreSQL + PostGIS
* [PostgreSQL](https://www.postgresql.org/download/)
* [PostGIS](https://postgis.net/install/)

### Install Python or Python Distribution
* [Python3](https://www.python.org/downloads/)
* [Anaconda](https://www.anaconda.com/products/distribution)


### Clone Django Project
Clone the GledSys repository
```
git clone https://github.com/fhabibie/GledSysDashboard.git
```

or you can download the ZIP file project
```
wget https://github.com/fhabibie/GledSysDashboard/archive/refs/heads/main.zip
```

### Connecting Django to PostGIS database
Setup database connection through ```settings.py```
```
...
# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': os.environ.get('POSTGRES_NAME'),
        'USER': os.environ.get('POSTGRES_USER'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
        'HOST': 'db',
        'PORT': 5432,
    }
}
```

### Install Django and its dependecies
Create python virtual env (virtualenv, conda env, or venv)
Using venv
```
python -m venv myenv
source myenv/bin/activate

```
Using conda 
```
conda create --name myenv
conda activate myenv

```

Install python dependencies
```
pip install -r gledsys\requirements.txt

# conda
conda install --file gledsys\requirements.txt
```
### Migrate Database
Migrate database
```
python manage.py makemigrations
python manage.py migrate
```
Create django-admin user
```
python manage.py createsuperuser
```


### Run Django Project
```
python manage.py runserver
```

## Usage
Run
```
docker-compose up
```
or
```
python manage.py runserver
```

## Feature
Lightning
- ??? Upload CSV files and bulk import to DB
- ??? Query by boundary box
- ??? Query by SHP files and saved SHP files
- ??? Plotting distribution points

Earthquake
- ?????? Upload CSV files and bulk import to DB
- ?????? Query by boundary box
- ?????? Query by SHP files and saved SHP files
- ?????? Plotting distribution points

Weather
- ?????? Upload CSV files and bulk import to DB
- ?????? Query by boundary box
- ?????? Query by SHP files and saved SHP files
- ?????? Plotting distribution points

Infographic and Visualization
- ?????? Daily Infographic
- ?????? Report and Bulletin
- ?????? Map Report

Data Catalog
- ?????? Data Catalog

## Built with
* Django
* PostGIS
* Plotly, Leaflet, PyGMT
* Bootstrap and SB Admin Template