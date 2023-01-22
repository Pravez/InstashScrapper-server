import logging
from typing import Tuple, Optional, Dict, List

from instagrapi import Client
from instagrapi.mixins.challenge import ChallengeChoice
from werkzeug.exceptions import Unauthorized


class Instagram:
    _username: str
    _client: Optional[Client]
    _has_credentials_in_config: bool

    def __init__(self):
        from .config import app

        self._client = None
        self._has_credentials_in_config = "INSTAGRAM" in app.config

    def try_logging(self, username: Optional[str] = None, password: Optional[str] = None) -> Tuple[bool, str]:
        if username is None or password is None:
            from .config import app

            logging.info("Try logging from config file ...")
            username = app.config["INSTAGRAM"]["USERNAME"]
            password = app.config["INSTAGRAM"]["PASSWORD"]
        self._username = username
        self._client = Client()
        self._client.challenge_code_handler = self._challenge_code_handler
        try:
            self._client.login(username, password)
            return True, ""
        except Exception as e:
            self._client = None
            return False, str(e)

    def get_hashtag_data(self, name: str) -> Dict:
        self._check_status()
        try:
            return self._client.hashtag_info(name).dict()
        except Exception as e:
            self._client = None
            raise Unauthorized(str(e))

    def get_related_hashtags(self, name: str) -> List[Dict]:
        self._check_status()
        return [h.dict() for h in self._client.hashtag_related_hashtags(name)]

    def _check_status(self):
        if self._client is None:
            if self._has_credentials_in_config:
                self.try_logging()
            else:
                raise Unauthorized("Not logged in")

    def status(self) -> bool:
        return self._client is not None

    @staticmethod
    def _challenge_code_handler(username, choice):
        if choice == ChallengeChoice.SMS:
            logging.error("Unable to handle the SMS challenge")
        elif choice == ChallengeChoice.EMAIL:
            from .email import get_code_from_email

            result = get_code_from_email(username)
            if result:
                return result
            logging.error("Unable to find the correct mail")
        return False
