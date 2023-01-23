from typing import List, Optional, Any, TypeVar

from flask import abort


def first_or_none(x: Optional[List]) -> Optional[Any]:
    return None if x is None else next(iter(x), None)


MT = TypeVar('MT')


def handle_missing(result: Optional[MT]) -> Optional[MT]:
    if result is None:
        abort(404)
    return result
