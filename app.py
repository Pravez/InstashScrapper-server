from flask import request, jsonify
from flask_restx import Resource, Api

from .modules import instagram, app, get_or_create_hashtag_check, get_or_create_hashtag_to_check

api = Api(app, version="0.1", title="InstashScrappAPI")


@api.route("/status")
class Status(Resource):
    def get(self):
        return jsonify(logged_in=instagram.status())


@api.route("/login")
class Login(Resource):

    def post(self):
        for field in ["username", "password"]:
            if field not in request.form or len(request.form[field]) <= 0:
                return jsonify(error="A field is required", field=field)

        stat, err = instagram.try_logging(request.form["username"], request.form["password"])
        return jsonify(status=stat, error=err)


@api.route("/hashtags/<string:name>")
class Hashtags(Resource):
    def get(self, name: str):
        refresh = request.args.get("refresh") == "true"
        hashtag = get_or_create_hashtag_check(name, refresh, persist=True)
        return jsonify(hashtag.serialize())

    def post(self, name: str):
        to_check = get_or_create_hashtag_to_check(name)
        return jsonify(to_check.serialize())
