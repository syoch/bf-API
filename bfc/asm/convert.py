from .platform import table
from typing import List


def convert(src: List[str]) -> List[str]:
    dest = []
    for line in src:
        tokens = line.split(" ")
        if line in table:
            dest += table[line]
        elif tokens[0] in table:
            dest += [line.format(int(tokens[1]))
                     for line in table[tokens[0]]]
        else:
            dest.append(line)
    return dest
