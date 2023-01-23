from dataclasses import dataclass
from datetime import datetime

from modules import HashtagToCheck, Category


@dataclass
class HashtagToCheckDto:
    id: int
    created: datetime
    name: str
    hashtag_id: str
    last_check: datetime
    media_count: int

    @staticmethod
    def from_entity(to_check: HashtagToCheck, hashtag):
        return HashtagToCheckDto(**to_check.serialize(), media_count=hashtag.media_count)


@dataclass
class CategoryDto:
    id: int
    created: datetime
    name: str
    related_hashtags: int

    @staticmethod
    def from_entity(category: Category):
        return CategoryDto(**category.serialize(), related_hashtags=len(category.hashtags))
