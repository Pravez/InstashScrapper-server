from typing import Tuple, Optional, Dict, List

from instagrapi import Client
from instagrapi.mixins.challenge import ChallengeChoice
from werkzeug.exceptions import Unauthorized
import logging


class Instagram:
    _username: str
    _client: Optional[Client]

    def __init__(self):
        self._client = None

    def try_logging(self, username: str, password: str) -> Tuple[bool, str]:
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
            raise Unauthorized("Not logged in")

    def status(self) -> bool:
        return self._client is not None

    @staticmethod
    def _challenge_code_handler(username, choice):
        if choice == ChallengeChoice.SMS:
            logging.error("Unable to handle the SMS challenge")
        elif choice == ChallengeChoice.EMAIL:
            # https://adw0rd.github.io/instagrapi/usage-guide/challenge_resolver.html
            logging.error("Unable to handle the Email challenge")
        return False
