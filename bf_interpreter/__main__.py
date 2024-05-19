import os

from lark import Lark, Transformer, UnexpectedEOF


class Runtime:
    def __init__(self):
        self.memory = [0]
        self.memory_length = 1
        self.pointer = 0

    def pointer_increment(self):
        self.pointer += 1
        if self.pointer == self.memory_length:
            self.memory.append(0)
            self.memory_length += 1

    def pointer_decrement(self):
        self.pointer -= 1
        if self.pointer < 0:
            raise Exception("Negative pointer")

    def value_increment(self):
        self.memory[self.pointer] += 1
        if self.memory[self.pointer] > 255:
            self.memory[self.pointer] = 0

    def value_decrement(self):
        self.memory[self.pointer] -= 1
        if self.memory[self.pointer] < 0:
            self.memory[self.pointer] = 255

    def value_output(self):
        print(chr(self.memory[self.pointer]), end="")

    def value_input(self):
        self.memory[self.pointer] = ord(input()[0])

    def get_value_at_pointer(self):
        return self.memory[self.pointer]


class MemoryViewer:
    def __init__(self, runtime: Runtime):
        self.runtime = runtime

        self.highlight_cycle = 6

    def show_memory(self):
        columns = self.highlight_cycle * 4

        for i, value in enumerate(self.runtime.memory):
            if i // self.highlight_cycle % 2 == 0:
                print("\033[1;32m", end="")
            else:
                print("\033[1;34m", end="")

            if i == self.runtime.pointer:
                print("\033[1;31m", end="")

            print(f"{value:3}", end=" ")
            print("\033[0m", end="")

            if i % (columns) == columns - 1:
                print()

        print()


class Inst:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return f"Inst({self.value})"

    def execute(self, runtime: Runtime):
        for inst in self.value:
            if inst == "+":
                runtime.value_increment()
            elif inst == "-":
                runtime.value_decrement()
            elif inst == ">":
                runtime.pointer_increment()
            elif inst == "<":
                runtime.pointer_decrement()
            elif inst == ".":
                runtime.value_output()
            elif inst == ",":
                runtime.value_input()


class Loop:
    def __init__(self, insts: list[Inst]):
        self.insts = insts

    def __str__(self):
        content = ", ".join(map(str, self.insts))

        return f"Loop({content})"

    def execute(self, runtime: Runtime):
        while runtime.get_value_at_pointer():
            for inst in self.insts:
                inst.execute(runtime)


class Program:
    def __init__(self, insts: list[Inst]):
        self.insts = insts

    def __str__(self):
        content = ", ".join(map(str, self.insts))

        return f"Program({content})"

    def execute(self, runtime: Runtime):
        for inst in self.insts:
            inst.execute(runtime)


class BFTransformer(Transformer):
    def start(self, tree):
        return Program(tree)

    def other(self, tree):
        return Inst("")

    def inst(self, tree):
        return Inst(tree[0])

    def loop(self, tree):
        return Loop(tree)


class App:
    def __init__(self):
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))

        with open(os.path.join(BASE_DIR, "bf.ebnf")) as f:
            grammer = f.read()
        self.parser = Lark(grammer)
        self.transformer = BFTransformer()

        self.runtime = Runtime()
        self.memory_viewer = MemoryViewer(self.runtime)

        self.buffer = ""

    def reset(self):
        self.runtime = Runtime()
        self.memory_viewer = MemoryViewer(self.runtime)

    def process(self, code):
        try:
            tree = self.parser.parse(self.buffer + code)
        except UnexpectedEOF:
            self.buffer += code
            return
        else:
            self.buffer = ""

        program = self.transformer.transform(tree)
        program.execute(self.runtime)

    def show_memory(self):
        self.memory_viewer.show_memory()


def interactive():
    app = App()

    while True:
        try:
            code = input(">>> ").strip()
        except EOFError:
            break

        if code == ".exit":
            break
        elif code == ".reset":
            app.reset()
        elif code == ".mem":
            app.show_memory()
        else:
            app.process(code)
        app.show_memory()


def run(filename: str):
    app = App()

    with open(filename) as f:
        code = f.read()

    app.process(code)

    app.show_memory()


def main():
    import sys

    if len(sys.argv) != 2:
        interactive()
    else:
        run(sys.argv[1])


if __name__ == "__main__":
    main()
