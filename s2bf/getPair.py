class Pair():
    def __init__(self, a: int, b: int):
        self.a = a
        self.b = b

    def get(self):
        if self.a == 1:
            return self.b
        if self.b == 1:
            return self.a

        return self.a+self.b+7


def getPair(val: int):
    pair = Pair(1, val)
    minscore = val**4
    minpair = Pair(1, 1)
    for i in range(1, val+1):
        if val % i == 0:
            pair.a = i
            pair.b = val/i
            if pair.get() < minscore:
                minscore = pair.get()
                minpair.a = pair.a
                minpair.b = pair.b
    return minpair
