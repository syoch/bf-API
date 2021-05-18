from typing import List


def pushPop(src: List[str]) -> List[str]:
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


def inc(src: List[str]) -> List[str]:
    ret = []
    inc = 0
    for line in src:
        if line == "inc":
            inc += 1
        else:
            if inc != 0:
                ret.append("add["+str(inc)+"]")
                inc = 0
            ret.append(line)
    return ret


def auto(src: List[str]) -> List[str]:
    ret = src
    ret = pushPop(ret)
    ret = inc(ret)
    return ret
