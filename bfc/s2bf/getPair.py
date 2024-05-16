class PairInt:
    def __init__(self, num: int):
        self.num = num

    def getscore(self):
        return self.num

    def __int__(self) -> int:
        return int(self.num)

    def __str__(self) -> str:
        return str(self.num)

    def get(self, ch) -> tuple[int, str]:
        s = -1 if ch == "-" else 1
        num = int(self.num)
        return 0, ("-" if s * num < 0 else "+") * abs(num)


class Pair:
    def __init__(self, a: int, b: int):
        self.a: PairInt = PairInt(a)
        self.b: PairInt = PairInt(b)
        self.offs: PairInt = PairInt(0)

    def __str__(self) -> str:
        return f"({self.a}*{self.b}+{self.offs})"

    def __int__(self) -> int:
        return self.a.num * self.b.num + self.offs.num

    def get(self, ch="+") -> tuple[int, str]:
        if self.a == 1:
            return 0, ch * (self.b.num + self.offs.num)
        if self.b == 1:
            return 0, ch * (self.a.num + self.offs.num)

        da, a = self.a.get("+")
        db, b = self.b.get(ch)
        sign_ch = -1 if ch == "-" else 1
        o = ("-" if sign_ch * self.offs.num < 0 else "+") * abs(self.offs.num)
        return max(da, db) + 1, f"{a}[<{b}>-]<{o}>"

    def getscore(self) -> int:
        if self.a == 1:
            return int(self.b) + abs(self.offs.num)
        if self.b == 1:
            return int(self.a) + abs(self.offs.num)

        return self.a.getscore() + self.b.getscore() + 7 + abs(self.offs.num)


def _getPair(val: int) -> Pair:
    if type(val) == PairInt:
        val = int(val)
    pair = Pair(1, val)
    minpair = Pair(1, val)
    for i in range(1, int(val**0.5) + 1):
        if val % i == 0:
            pair.a = PairInt(i)
            pair.b = PairInt(val // i)
            if pair.getscore() < minpair.getscore():
                minpair = pair
    pair = minpair

    return minpair


def getPair(val: int):
    if type(val) == PairInt:
        val = int(val)
    pair = Pair(1, val)
    minpair = Pair(1, val)
    for i in range(-val, val, 1):
        pair = _getPair(val - i)
        pair.offs = PairInt(i)

        if pair.getscore() < minpair.getscore():
            minpair = pair
    pair = minpair
    if int(pair.a) != 1 and int(pair.b) != 1:
        if int(pair.a) >= 10:
            test = getPair(int(pair.a))
            if test.getscore() < pair.a.getscore():
                pair.a = PairInt(int(test))
        if int(pair.b) >= 10:
            test = getPair(int(pair.b))
            if test.getscore() < pair.b.getscore():
                pair.b = test
    return pair
