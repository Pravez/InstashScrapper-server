from typing import List, Optional, Any


def first_or_none(x: Optional[List]) -> Optional[Any]:
    return None if x is None else next(iter(x), None)
