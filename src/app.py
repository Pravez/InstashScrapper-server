from flask import request, jsonify, abort
from flask_restx import Resource, Api
from werkzeug.exceptions import SecurityError

from modules import instagram, app, get_or_create_hashtag_check, get_or_create_hashtag_to_check, get_hashtag_to_check, \
    get_hashtags_to_check, get_hashtag_check_for
from dto import *

api = Api(app, version="0.1", title="InstashScrappAPI")

from models import *


@api.route("/status")
class Status(Resource):
    def get(self):
        return jsonify(logged_in=instagram.status())


login_parser = api.parser()
login_parser.add_argument("username", type=str, location='json', required=True)
login_parser.add_argument("password", type=str, location='json', required=True)


@api.route("/login")
class Login(Resource):

    @api.expect(login_parser)
    def post(self):
        args = login_parser.parse_args()
        stat, err = instagram.try_logging(args["username"], args["password"])
        if "ChallengeResolve" in err:
            raise SecurityError("You need to resolve the challenge on instagram.com")
        return jsonify(status=stat)


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
            abort(404)
        return HashtagToCheckDto.from_entity(to_check, get_hashtag_check_for(to_check.name, to_check.last_check))

    @api.marshal_with(hashtag_to_check_model)
    def post(self, name: str):
        to_check = get_or_create_hashtag_to_check(name)
        return to_check


@api.route("/checks")
class Checks(Resource):
    @api.marshal_list_with(hashtag_to_check_model)
    def get(self):
        return [HashtagToCheckDto.from_entity(t, get_hashtag_check_for(t.name, t.last_check)) for t in
                get_hashtags_to_check()]


if __name__ == "__main__":
    app.run(debug=True)
