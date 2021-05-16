from . import getPair
import numpy as np


def get(val: int):
    if val == 0:
        return ""

    sign = np.sign(val)

    d, p = getPair.getPair(sign*val).get(
        "-" if sign == -1 else "+"
    )
    return ">"*d+p+"<"*d
