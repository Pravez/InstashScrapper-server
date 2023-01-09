from dataclasses import dataclass
from datetime import datetime

from flask import request, jsonify
from flask_restx import Resource, Api, fields

from modules import instagram, app, get_or_create_hashtag_check, get_or_create_hashtag_to_check, get_hashtag_to_check, \
    get_hashtags_to_check, get_hashtag_check_for
from modules.database import HashtagToCheck

api = Api(app, version="0.1", title="InstashScrappAPI")

base_hashtag_model = api.model("BaseHashtag", {
    "id": fields.Integer,
    "name": fields.String,
    "media_count": fields.Integer
})

hashtag_check_model = api.model("HashtagCheck", {
    "id": fields.Integer,
    "time": fields.DateTime,
    "name": fields.String,
    "media_count": fields.Integer
})

hashtag_to_check_model = api.model("HashtagToCheck", {
    "id": fields.Integer,
    "created": fields.DateTime,
    "name": fields.String,
    "hashtag_id": fields.String,
    "last_check": fields.DateTime,
    "media_count": fields.Integer
})


@dataclass
class HashtagToCheckDto:
    id: int
    created: datetime
    name: str
    hashtag_id: str
    last_check: datetime
    media_count: int


@api.route("/status")
class Status(Resource):
    def get(self):
        return jsonify(logged_in=instagram.status())

login_parser = api.parser()
login_parser.add_argument("username", type=str, location='form', required=True)
login_parser.add_argument("password", type=str, location='form', required=True)

@api.route("/login")
class Login(Resource):

    @api.expect(login_parser)
    def post(self):
        args = login_parser.parse_args()
        stat, err = instagram.try_logging(args["username"], args["password"])
        return jsonify(status=stat, error=err)


@api.route("/hashtags/<string:name>")
class Hashtags(Resource):
    @api.marshal_with(hashtag_check_model)
    def get(self, name: str):
        refresh = request.args.get("refresh") == "true"
        hashtag = get_or_create_hashtag_check(name, refresh, persist=True)
        return hashtag


@api.route("/hashtags/<string:name>/related")
class RelatedHashtags(Resource):
    @api.marshal_list_with(base_hashtag_model)
    def get(self, name: str):
        return instagram.get_related_hashtags(name)


@api.route("/checks/<string:name>")
class Check(Resource):
    @api.marshal_with(hashtag_to_check_model)
    def get(self, name: str):
        to_check = get_hashtag_to_check(name)
        if to_check is None:
            return {}, 404
        return to_dto(to_check)

    @api.marshal_with(hashtag_to_check_model)
    def post(self, name: str):
        to_check = get_or_create_hashtag_to_check(name)
        return to_check


@api.route("/checks")
class Checks(Resource):
    @api.marshal_list_with(hashtag_to_check_model)
    def get(self):
        return [to_dto(t) for t in get_hashtags_to_check()]


def to_dto(to_check: HashtagToCheck) -> HashtagToCheckDto:
    hashtag = get_hashtag_check_for(to_check.name, to_check.last_check)
    return HashtagToCheckDto(**to_check.serialize(), media_count=hashtag.media_count)


if __name__ == "__main__":
    app.run(debug=True)
