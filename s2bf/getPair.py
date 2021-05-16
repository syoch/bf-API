class pair():
    def __init__(self, a: int, b: int):
        self.a = a
        self.b = b

    def get(self):
        if self.a == 1:
            return self.b
        if self.b == 1:
            return self.a

        return self.a+self.b+7
