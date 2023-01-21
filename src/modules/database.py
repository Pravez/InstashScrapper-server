from typing import Optional, Any, List

from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import inspect

from . import first_or_none
from .config import app

db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Serializer(object):
    def serialize(self):
        return {c: getattr(self, c) for c in inspect(self).attrs.keys()}

    @staticmethod
    def serialize_list(s_list):
        return [m.serialize() for m in s_list]


class HashtagCheck(db.Model, Serializer):
    id = db.Column(db.String(128), nullable=False)
    time = db.Column(db.TIMESTAMP(timezone=True), nullable=False, primary_key=True)
    name = db.Column(db.String(512), nullable=False)
    media_count = db.Column(db.Integer, nullable=False)


class HashtagToCheck(db.Model, Serializer):
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, nullable=False)
    name = db.Column(db.String(512), nullable=False, unique=True)
    hashtag_id = db.Column(db.String(128))
    last_check = db.Column(db.DateTime)


transaction = db.session.execute


def get_one(t) -> Optional[Any]:
    return first_or_none(transaction(t.limit(1)).fetchone())


def get_all(t) -> List:
    return transaction(t).scalars().all()


def exists(t) -> bool:
    value = get_one(t)
    return value is not None and value > 0


def add(d):
    db.session.add(d)
    db.session.commit()


def commit():
    db.session.commit()
