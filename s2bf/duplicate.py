from typing import Iterable
import collections


def getDuplicate(itr: Iterable):
    counter = collections.Counter(itr)
    duplicate = []
    for a in counter:
        if counter[a] > 1:
            duplicate.append(a)
    return duplicate
