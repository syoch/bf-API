from s2bf.duplicate import getDuplicate
from . import diffArray, pairGet, remover
import sys
src = sys.argv[1]
out = ""
duplicates = getDuplicate(src)
table = {}
ptr = 0
prev = 0
arr = diffArray.asciiArray(src)
for ind, _ch in enumerate(arr):
    if ind == len(arr)-1:
        nex = None
    else:
        nex = chr(arr[ind+1])
    ch = chr(_ch)
    if ch in table:  # use shotcut
        off = table[ch]-ptr
        out += ("<" if off < 0 else ">")*abs(off)
        out += "."
        out += (">" if off < 0 else "<")*abs(off)
    else:
        out += pairGet.get(_ch-prev)
        out += "."
        if ch in duplicates:
            out += "[>+>+<<-]>>[<<+>>-]<"
            table[ch] = ptr
            ptr += 1
        prev = _ch
# print(table)
print(remover.auto(out))
