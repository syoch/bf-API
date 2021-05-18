from typing import List


def dest(src: List[str]) -> List[str]:
    ret = []
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
            ret.append(line)
    return ret


def auto(src: List[str]) -> List[str]:
    ret = src
    ret = dest(src)
    return ret
