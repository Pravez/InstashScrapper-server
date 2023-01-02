from typing import List, Any, Optional

from ..modules import first_or_none
from .database import db

transaction = db.session.execute


def get_one(t) -> Optional[Any]:
    return first_or_none(transaction(t.limit(1)).fetchone())


def get_all(t) -> List:
    return transaction(t).fetchall()


def exists(t) -> bool:
    value = get_one(t)
    return value is not None and value > 0


def add(d):
    db.session.add(d)
    db.session.commit()