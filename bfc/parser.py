from _typeshed import NoneType
from typing import Any, Tuple


class parser():
    def __init__(self):
        self.src = ""
        self.index = 0

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

    def except(self, ch: str) -> NoneType:
        if self.consume(ch)[0] == False:
            raise Exception(f"excepted {ch}")

    def loop(self):
        stmts = ""
        self.except("[")
        while self.peek() != "]":
            stmts += self.stmt()
        self.except("[")
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
