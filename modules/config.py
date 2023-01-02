import toml
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from .instagram import Instagram

app = Flask(__name__)
app.config.from_file("../resources/config.toml", load=toml.load)

db_conf = app.config["DATABASE"]
app.config[
    "SQLALCHEMY_DATABASE_URI"] = f"postgresql+psycopg2://{db_conf['USER']}:{db_conf['PASSWORD']}@{db_conf['HOST']}:{db_conf['PORT']}/{db_conf['DB']}"
db = SQLAlchemy(app)
migrate = Migrate(app, db)

instagram = Instagram()
