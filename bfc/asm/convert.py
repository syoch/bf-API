from .table import table
from typing import List


def convert(src: List[str]) -> List[str]:
    dest = []
    for line in src:
        if line in table:
            dest.append(table[line])
        else:
            dest.append(line)
    return dest
