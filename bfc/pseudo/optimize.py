from typing import List


def auto(src: List[str]) -> List[str]:
    dest = []
    nex = ""
    skip = 0
    for i in range(len(src)):
        if skip:
            skip -= 1
            continue

        line = src[i]
        if len(src) == i+1:
            nex = ""
        else:
            nex = src[i+1]

        if line == "push" and nex == "pop":
            skip = 1
            pass
        else:
            dest.append(line)
    return dest
