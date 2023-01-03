from flask import request, jsonify

from .modules import instagram, app, get_or_create_hashtag_check, get_or_create_hashtag_to_check


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
    hashtag = get_or_create_hashtag_check(name, refresh, persist=True)
    return jsonify(hashtag.serialize())


@app.post("/hashtags/<string:name>")
def set_hashtag_to_check(name: str):
    to_check = get_or_create_hashtag_to_check(name)
    return jsonify(to_check.serialize())
