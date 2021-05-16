from . import getPair


def get(val: int):
    if val == "":
        return ""
    elif val < 0:
        d, p = getPair.getPair(-val).get("-")
    else:
        d, p = getPair.getPair(val).get()
    return ">"*d+p+"<"*d
