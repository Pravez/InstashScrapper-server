import time

from flask import request, jsonify

from .modules import instagram, app, db
from .database import HashtagCheck, HashtagToCheck

transaction = db.session.execute


@app.get("/")
def hello_world():
    return "<p>Holy hell, it works !</p>"


@app.get("/status")
def status():
    return jsonify(logged_in=instagram.status())


@app.post("/login")
def login():
    for field in ["username", "password"]:
        if field not in request.form or len(request.form[field]) <= 0:
            return jsonify(error="A field is required", field=field)

    stat, err = instagram.try_logging(request.form["username"], request.form["password"])
    return jsonify(status=stat, error=err)


@app.get("/hashtags/<string:name>")
def get_hashtag_data(name: str):
    refresh = request.args.get("refresh", type=bool)
    exists = \
        db.session.execute(db.select(db.func.count(HashtagCheck.name)).filter(HashtagCheck.name == name)).fetchone()[0]
    if exists == 0:
        refresh = True
    if refresh is True:
        data = instagram.get_hashtag_data(name)
        hashtag = HashtagCheck(
            id=data["id"],
            time=time.time(),
            name=name,
            mentions_counts=data["mentions_count"]
        )
        db.session.add(hashtag)
    else:
        hashtag = db.session.execute(
            db.select(HashtagCheck).filter(HashtagCheck.name == name).order_by(HashtagCheck.time).limit(1))
    return jsonify(
        id=hashtag.id,
        time=hashtag.time,
        name=hashtag.name,
        mentions_count=hashtag.mentions_count
    )


@app.post("/hashtags/<string:name>")
def set_hashtag_to_check(name: str):
    exists = \
        transaction(
            db.select(db.func.count(HashtagToCheck.name)).filter(HashtagToCheck.name == name)).fetchone()[0]
    if exists == 0:
        hashtag = HashtagToCheck(created=time.time(), name=name)
    else:
        hashtag = transaction(db.select(HashtagToCheck).filter(HashtagToCheck.name == name)).fetchone()[0]
    return jsonify(
        id=hashtag.id,
        name=hashtag.name,
        created=hashtag.created,
        last_check=hashtag.last_check
    )
