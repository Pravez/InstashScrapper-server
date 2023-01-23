from typing import Dict, Any, Optional

from flask import abort
from flask_restx import Resource, Api
from werkzeug.exceptions import SecurityError, Unauthorized

from modules import instagram, app, get_or_create_hashtag_check, get_or_create_hashtag_to_check, get_hashtag_to_check, \
    get_hashtags_to_check, get_hashtag_check_for, get_history_for_hashtag_check, delete_hashtag_to_check, \
    get_categories, get_category, handle_missing
from dto import *

api = Api(app, version="0.1", title="InstashScrappAPI")

from models import *
from cron import crontab


@api.route("/status")
class Status(Resource):
    @api.marshal_with(login_status_model)
    def get(self):
        return {"logged_in": instagram.status()}


login_parser = api.parser()
login_parser.add_argument("username", type=str, location='json', required=True)
login_parser.add_argument("password", type=str, location='json', required=True)

hashtags_get_parser = api.parser()
hashtags_get_parser.add_argument("refresh", type=bool, location="args")


@api.route("/login")
class Login(Resource):

    @api.expect(login_parser)
    @api.marshal_with(login_result_model)
    def post(self):
        args = login_parser.parse_args()
        stat, err = instagram.try_logging(args["username"], args["password"])
        if "ChallengeResolve" in err:
            raise SecurityError("You need to resolve the challenge on instagram.com")
        if not stat:
            raise Unauthorized(err)
        return {"status": stat}


############################################################
################## HASHTAGS ################################

@api.route("/hashtags/<string:name>")
class Hashtags(Resource):
    @api.expect(hashtags_get_parser)
    @api.marshal_with(hashtag_check_model)
    def get(self, name: str):
        args = hashtags_get_parser.parse_args()
        refresh = args.get("refresh", False)
        hashtag = get_or_create_hashtag_check(name, refresh if refresh is not None else False, persist=True)
        return hashtag


@api.route("/hashtags/<string:name>/history")
class HashtagsHistory(Resource):
    @api.marshal_list_with(hashtag_check_model)
    def get(self, name: str):
        hashtags = get_history_for_hashtag_check(name)
        return hashtags


@api.route("/hashtags/<string:name>/related")
class RelatedHashtags(Resource):
    @api.marshal_list_with(base_hashtag_model)
    def get(self, name: str):
        return instagram.get_related_hashtags(name)


############################################################
################## HASHTAGS TO CHECK #######################


@api.route("/checks/<string:name>")
class Check(Resource):
    @api.marshal_with(hashtag_to_check_model)
    def get(self, name: str):
        to_check = handle_missing(get_hashtag_to_check(name))
        return HashtagToCheckDto.from_entity(to_check, get_hashtag_check_for(to_check.name, to_check.last_check))

    @api.marshal_with(hashtag_to_check_model)
    def post(self, name: str):
        to_check = get_or_create_hashtag_to_check(name)
        return to_check

    @api.marshal_with(delete_result_model)
    def delete(self, name: str):
        return {"deleted": delete_hashtag_to_check(name)}


@api.route("/checks")
class Checks(Resource):
    @api.marshal_list_with(hashtag_to_check_model)
    def get(self):
        return [HashtagToCheckDto.from_entity(t, get_hashtag_check_for(t.name, t.last_check)) for t in
                get_hashtags_to_check()]


############################################################
###################### CATEGORIES ##########################

@api.route("/category")
class Categories(Resource):
    @api.marshal_list_with(category_list_model)
    def get(self):
        categories = get_categories()
        return [CategoryDto.from_entity(c) for c in categories]


@api.route("/category/<int:category_id>")
class Category(Resource):
    @api.marshal_with(category_model)
    def get(self, category_id: int):
        category = handle_missing(get_category(category_id))
        return category


if __name__ == "__main__":
    app.run(debug=True)
