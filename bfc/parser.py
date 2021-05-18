from typing import Any, Tuple


class parser():
    def __init__(self, src):
        self.src = src
        self.index = 0

    def hasData(self):
        if len(self.src) <= self.index:
            return False
        else:
            return True

    def peek(self):
        if len(self.src) <= self.index:
            return None
        else:
            return self.src[self.index]

    def next(self):
        self.index += 1
        if len(self.src) <= self.index:
            return None
        else:
            return self.src[self.index]

    def consume(self, ch: str) -> Tuple[bool, Any]:
        if self.peek() == ch:
            self.index += 1
            return True, ch
        else:
            return False, None

    def Except(self, ch: str) -> None:
        if self.consume(ch)[0] == False:
            raise Exception(f"Excepted {ch}")

    def loop(self):
        stmts = ""
        self.Except("[")
        while self.peek() != "]":
            stmts += self.stmt()
        self.Except("[")
        return stmts

    def stmt(self):
        while self.peek() not in "+-<>.,":
            self.index += 1
        if self.next() == "[":
            return self.loop()
        else:
            return self.next()

    def parse(self):
        stmts = []
        while self.hasData():
            stmts.append(self.stmt())
        return stmts
