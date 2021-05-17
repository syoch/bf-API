from s2bf.duplicate import getDuplicate
from . import diffArray, pairGet, remover
import sys
src = sys.argv[1]
out = ""
duplicates = getDuplicate(src)
table = {}
for (ch, diff) in zip(*diffArray.diffArray(src)):
    print(ch, diff)
    out += pairGet.get(diff)+"."
print(remover.auto(out))
