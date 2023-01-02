from typing import Tuple, Optional, Dict

from instagrapi import Client

class Instagram:
    _username: str
    _client: Optional[Client]

    def __init__(self):
        self._client = None

    def try_logging(self, username: str, password: str) -> Tuple[bool, str]:
        self._username = username
        self._client = Client()
        try:
            self._client.login(username, password)
            return True, ""
        except Exception as e:
            self._client = None
            return False, str(e)

    def get_hashtag_data(self, name: str) -> Dict:
        if self._client is None:
            raise SystemError("Not logged in")
        return self._client.hashtag_info(name).dict()

    def status(self) -> bool:
        return self._client is not None
