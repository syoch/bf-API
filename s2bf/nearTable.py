from typing import Mapping
from . import diffArray


def get(src: str) -> Mapping[int, int]:
    asciiList = diffArray.asciiArray(src)
    _table = {}
    prev = 0
    for asc in asciiList:
        if asc+1 in asciiList or asc-1 in asciiList:
            _table[prev] = asc
        prev = asc
    return _table
