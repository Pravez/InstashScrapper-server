from flask_restx import fields
from app import api

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

login_result_model = api.model("LoginResult", {
    "status": fields.Boolean
})

login_status_model = api.model("LoginStatus", {
    "logged_in": fields.Boolean
})
