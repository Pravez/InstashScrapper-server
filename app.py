import time

from flask import request, jsonify
import datetime

from .modules import instagram, app, db
from .database import HashtagCheck, HashtagToCheck, get_one, get_all, exists, add

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
    refresh = request.args.get("refresh") == "true"
    if exists(db.select(db.func.count(HashtagCheck.name)).filter(HashtagCheck.name == name)) is False:
        refresh = True
    if refresh is True:
        data = instagram.get_hashtag_data(name)
        hashtag = HashtagCheck(
            id=data["id"],
            time=datetime.datetime.now(),
            name=name,
            media_count=data["media_count"]
        )
        add(hashtag)
    else:
        hashtag = get_one(db.select(HashtagCheck).filter(HashtagCheck.name == name).order_by(HashtagCheck.time.desc()))
    return jsonify(
        id=hashtag.id,
        time=hashtag.time,
        name=hashtag.name,
        media_count=hashtag.media_count
    )


@app.post("/hashtags/<string:name>")
def set_hashtag_to_check(name: str):
    if exists(db.select(db.func.count(HashtagToCheck.name)).filter(HashtagToCheck.name == name)) is False:
        hashtag = HashtagToCheck(created=datetime.datetime.now(), name=name)
        if exists(db.select(db.func.count(HashtagCheck.name)).filter(HashtagCheck.name == name)) is False:
            data = instagram.get_hashtag_data(name)
            hashtag.last_check = datetime.datetime.now()
            hashtag.hashtag_id = data["id"]
        else:
            hashtag_data = get_one(
                db.select(HashtagCheck).filter(HashtagCheck.name == name).order_by(HashtagCheck.time.desc()))
            hashtag.last_check = hashtag_data.time
            hashtag.hashtag_id = hashtag_data.id
        add(hashtag)
    else:
        hashtag = get_one(db.select(HashtagToCheck).filter(HashtagToCheck.name == name))
    return jsonify(
        id=hashtag.id,
        name=hashtag.name,
        created=hashtag.created,
        last_check=hashtag.last_check
    )
