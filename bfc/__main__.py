from pathlib import Path
from lark import Lark
from lark import Transformer
from lark import Tree


class StackMachineRaw(Transformer):
    def int(self, tree):
        return int(tree[0].value)

    def p_offset(self, tree):
        return tree[0]

    def n_offset(self, tree):
        return -tree[0]

    def stmt_add(self, tree):
        return "+" * tree[0]

    def stmt_zero(self, tree):
        return "[-]"

    def stmt_move(self, tree):
        offset = tree[0]

        return ("<" if offset < 0 else ">") * abs(offset)

    def program(self, tree):
        return tree


def main():
    BASE_DIR = Path(__file__).resolve().parent
    with open(BASE_DIR / "smr.ebnf") as f:
        grammar = f.read()
    parser = Lark(grammar, start="program")

    with open(BASE_DIR / "test-src" / "a.bfc-smr") as f:
        src = f.read()
    parser = Lark(grammar, start="program")

    tree = parser.parse(src)

    bfc = StackMachineRaw()
    ast = bfc.transform(tree)
    print("".join(map(str, ast)))


if __name__ == "__main__":
    main()
