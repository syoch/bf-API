from . import diffArray, pairGet, remover
import sys
src = sys.argv[1]
out = ""
for diff in diffArray.diffArray(src):
    out += pairGet.get(diff)+"."
print(remover.auto(out))
