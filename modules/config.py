import toml
import os
from flask import Flask
from logging.config import dictConfig
from .instagram import Instagram

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})


app = Flask(__name__)
env_file = os.getenv("APPSETTINGS_FILE", "config-local.toml")
app.config.from_file(f"../resources/{env_file}", load=toml.load)

db_conf = app.config["DATABASE"]
app.config[
    "SQLALCHEMY_DATABASE_URI"] = f"postgresql+psycopg2://{db_conf['USER']}:{db_conf['PASSWORD']}@{db_conf['HOST']}:{db_conf['PORT']}/{db_conf['DB']}"


instagram = Instagram()
