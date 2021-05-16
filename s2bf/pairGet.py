from . import getPair


def get(val: int):
    d, p = getPair.getPair(val).get()
    return ">"*d+p+"<"*d
