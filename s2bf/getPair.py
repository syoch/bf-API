class Pair():
    def __init__(self, a: int, b: int):
        self.a = a
        self.b = b
        self.offs = 0

    def __str__(self) -> str:
        return f"({self.a}*{self.b}+{self.offs})"

    def get(self, ch="+"):
        if self.a == 1:
            return 0, ch*(self.b+self.offs)
        if self.b == 1:
            return 0, ch*(self.a+self.offs)

        da, a = getPair(self.a).get()
        db, b = getPair(self.b).get()
        o = ch*self.offs
        return max(da, db)+1, f"{a}[<{b}>-]<{o}>"

    def getscore(self):
        if self.a == 1:
            return self.b+self.offs
        if self.b == 1:
            return self.a+self.offs

        return self.a+self.b+7+self.offs


def getPair(val: int):
    pair = Pair(1, val)
    minscore = val**4
    minpair = Pair(1, 1)
    for i in range(1, int(val**.5)+1):
        if val % i == 0:
            pair.a = i
            pair.b = val/i
            if pair.getscore() < minscore:
                minscore = pair.getscore()
                minpair.a = pair.a
                minpair.b = pair.b
    if abs(minpair.a-minpair.b)+minpair.getscore() > 20:
        minpair = getPair(val-1)
        minpair.offs += 1

    return minpair
