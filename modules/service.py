from datetime import datetime
from typing import List

from .database import HashtagCheck, exists, get_one, add, HashtagToCheck, db, get_all
from .config import instagram


def get_or_create_hashtag_check(name: str, refresh: bool = False, persist: bool = False) -> HashtagCheck:
    if exists(db.select(db.func.count(HashtagCheck.name)).filter(HashtagCheck.name == name)) is False or refresh:
        data = instagram.get_hashtag_data(name)
        hashtag = HashtagCheck(
            id=data["id"],
            time=datetime.now(),
            name=name,
            media_count=data["media_count"]
        )
        if persist:
            add(hashtag)
    else:
        hashtag = get_one(db.select(HashtagCheck).filter(HashtagCheck.name == name).order_by(HashtagCheck.time.desc()))
    return hashtag


def get_hashtag_to_check(name: str) -> HashtagToCheck:
    return get_one(db.select(HashtagToCheck).filter(HashtagToCheck.name == name))


def get_hashtags_to_check() -> List[HashtagToCheck]:
    return get_all(db.select(HashtagToCheck))


def get_hashtag_check_for(name: str, date: datetime) -> HashtagCheck:
    return get_one(db.select(HashtagCheck).filter(HashtagCheck.name == name, HashtagCheck.time == date))


def get_or_create_hashtag_to_check(name: str) -> HashtagToCheck:
    if exists(db.select(db.func.count(HashtagToCheck.name)).filter(HashtagToCheck.name == name)) is False:
        hashtag = get_or_create_hashtag_check(name, persist=True)
        to_check = HashtagToCheck(
            created=datetime.now(),
            name=name,
            hashtag_id=hashtag.id,
            last_check=hashtag.time
        )
        add(to_check)
    else:
        to_check = get_one(db.select(HashtagToCheck).filter(HashtagToCheck.name == name))
    return to_check


