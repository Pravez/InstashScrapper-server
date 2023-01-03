# InstashScrapper

> A badly named project

The objective of this project is to provide a wrapper-like server
with some historization capacity around [Instagrapi](https://pypi.org/project/instagrapi/), a Python library 
to use the Instagram Private API. Let's query hashtags !

## Getting Started

First, install dependencies :
```shell
pip install -r requirements.txt
```

Then, start your server !

```shell
python3 -m flask run
```

## Database access

Data is stored inside a Database (really ?), so you need to
provide some credentials, which you can find in the [config file](resources/config.toml).

You can use the [docker-compose](dep/docker-compose.yml) file to start a TimescaleDB database.

## Database versioning

To apply database [migrations](migrations/versions), simply use flask :
```shell
python3 -m flask db upgrade
```