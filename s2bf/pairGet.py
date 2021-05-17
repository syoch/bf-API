from . import getPair
import numpy as np


def get(val: int):
    if val == 0:
        return ""

    sign = np.sign(val)

    pair = getPair.getPair(sign*val)
    pair.adjust()
    d, p = pair.get(
        "-" if sign == -1 else "+"
    )
    return ">"*d+p+"<"*d
