from ..modules import db


class HashtagCheck(db.Model):
    id = db.Column(db.Integer, nullable=False)
    time = db.Column(db.TIMESTAMP(timezone=True), nullable=False, primary_key=True)
    name = db.Column(db.String(512), nullable=False)
    mentions_count = db.Column(db.Integer, nullable=False)


class HashtagToCheck(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, nullable=False)
    name = db.Column(db.String(512), nullable=False)
    last_check = db.Column(db.DateTime)

