import numpy as np


def asciiArray(src: str):
    return [ord(ch) for ch in src]


def diffArray(src: str):
    ascArr = asciiArray(src)
    return [ascArr[0], *np.diff(ascArr)]
