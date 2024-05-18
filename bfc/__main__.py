from pathlib import Path
from typing import NewType
from lark import Lark
from lark import Transformer
from .s2bf.remover import auto as optimize

CELL_FORMAT = [
    "c/f",
    "c/t",
    "c/i",
    "c/v",
    "c/w0",
    "c/w1",
]


CELL_SIZE = 6
CellName = NewType("CellName", str)
CellIndex = NewType("CellIndex", int)


class Context:
    def __init__(self) -> None:
        self.pointer = 0
        self.variables: dict[CellName, CellIndex] = {}

    def move(self, offset: int) -> str:
        self.pointer += offset

        return ("<" if offset < 0 else ">") * abs(offset)

    def move_to(self, pointer: "Context") -> str:
        offset = pointer.pointer - self.pointer
        self.pointer = pointer.pointer

        return ("<" if offset < 0 else ">") * abs(offset)

    def incell_offset(self) -> int:
        return self.pointer % CELL_SIZE

    def cell_offset(self) -> int:
        return self.pointer // CELL_SIZE

    def clone(self) -> "Context":
        ret = Context()
        ret.pointer = self.pointer

        return ret

    def register_variable(self, name: CellName) -> CellIndex:
        index = CellIndex(len(self.variables))

        self.variables[name] = index

        return index

    def get_variable(self, name: CellName) -> CellIndex:
        return self.variables[name]


class AST:
    def bf_code(self, pointer: Context) -> str:
        raise NotImplementedError()


class TapeRef(AST):
    def offset(self, pointer: Context) -> int:
        raise NotImplementedError()


class TapeRefReversed(AST):
    def __init__(self, ref: TapeRef) -> None:
        self.ref = ref

    def bf_code(self, pointer: Context) -> str:
        code = self.ref.bf_code(pointer)
        code = code.replace("<", "X").replace(">", "<").replace("X", ">")

        return code

    def offset(self, pointer: Context) -> int:
        return -self.ref.offset(pointer)

    def __str__(self) -> str:
        return f"-{self.ref}"


class TapeRefLabel(TapeRef):
    def __init__(self, label: str) -> None:
        self.label = label

    def bf_code(self, pointer: Context) -> str:
        offset = self.offset(pointer)
        return pointer.move(offset)

    def offset(self, pointer: Context) -> int:
        target_incell_offset = CELL_FORMAT.index(self.label)
        current_incell_offset = pointer.incell_offset()

        offset = target_incell_offset - current_incell_offset

        return offset

    def __str__(self) -> str:
        return self.label


class TapeRefOffset(TapeRef):
    def __init__(self, offset: int) -> None:
        self.move_offset = offset

    def bf_code(self, pointer: Context) -> str:
        return pointer.move(self.move_offset)

    def offset(self, pointer: Context) -> int:
        return self.move_offset


class Stmt(AST):
    pass


class CodeBlock(Stmt):
    def __init__(self, stmts: list[Stmt]) -> None:
        self.stmts = stmts

    def bf_code(self, pointer: Context) -> str:
        code = ""
        for stmt in self.stmts:
            code += stmt.bf_code(pointer)

        return code

    def __str__(self) -> str:
        return "{\n" + ";\n".join(["  " + str(stmt) for stmt in self.stmts]) + "\n}"


class CodeEmit(Stmt):
    def __init__(self, code: str) -> None:
        self.code = code

    def bf_code(self, pointer: Context) -> str:
        return self.code

    def __str__(self) -> str:
        return f"emit {repr(self.code)}"


class TapeMove(Stmt):
    def __init__(self, offset: TapeRef) -> None:
        self.offset = offset

    def bf_code(self, pointer: Context) -> str:
        return self.offset.bf_code(pointer)


class TapeZero(Stmt):
    def bf_code(self, pointer: Context) -> str:
        return "[-]"

    def __str__(self) -> str:
        return "tape.zero"


class TapeAdd(Stmt):
    def __init__(self, value) -> None:
        self.value = value

    def bf_code(self, pointer: Context) -> str:
        return "+" * self.value

    def __str__(self) -> str:
        return f"tape.add {self.value}"


class TapeSub(Stmt):
    def __init__(self, value) -> None:
        self.value = value

    def bf_code(self, pointer: Context) -> str:
        return "-" * self.value


class TapeAddTo(Stmt):
    def __init__(self, dest_offsets: list[TapeRef]) -> None:
        self.dest_offsets = dest_offsets

    def bf_code(self, pointer: Context) -> str:
        offsets = sorted(self.dest_offsets, key=lambda x: x.offset(pointer))
        if not offsets:
            return ""

        previous_pointer = pointer.clone()

        code = "-"
        for offset in offsets:
            code += pointer.move(offset.offset(pointer))
            code += "+"

        code += pointer.move_to(previous_pointer)

        code = "[" + code + "]"

        return code


class TapeCopy(Stmt):
    def __init__(self, dest_offsets: list[TapeRef], trash_offset: TapeRef) -> None:
        self.dest_offsets = dest_offsets
        self.trash_offset = trash_offset

    def bf_code(self, pointer: Context) -> str:
        previous_pointer = pointer.clone()
        base = TapeRefLabel(CELL_FORMAT[pointer.incell_offset()])

        ret = ""
        ret += TapeAddTo(
            [
                *self.dest_offsets,
                self.trash_offset,
            ]
        ).bf_code(pointer)
        ret += TapePrefixRunin(self.trash_offset, TapeAddTo([base])).bf_code(pointer)

        pointer.move_to(previous_pointer)

        return ret

    def __str__(self) -> str:
        dest_str = " ".join([str(offset) for offset in self.dest_offsets])
        return f"copy -> [{dest_str}] using {self.trash_offset}"


class TapePrefix(Stmt):
    def __init__(self, offset: TapeRef, code: Stmt) -> None:
        self.offset = offset
        self.code = code


class TapePrefixRunin(TapePrefix):
    def bf_code(self, pointer: Context) -> str:
        code = self.offset.bf_code(pointer)
        code += self.code.bf_code(pointer)

        return code

    def __str__(self) -> str:
        return f"{self.offset}: loop {self.code}"


class TapePrefixLoop(TapePrefix):
    def bf_code(self, pointer: Context) -> str:
        code = self.offset.bf_code(pointer)
        code += "["
        code += self.code.bf_code(pointer)
        code += TapeMove(self.offset).bf_code(pointer)
        code += "]"

        return code


class TapePrefixIfThen(TapePrefix):
    def bf_code(self, pointer: Context) -> str:
        code = self.offset.bf_code(pointer)
        code += "[[-]"
        code += self.code.bf_code(pointer)
        code += "]"

        return code


class CellNew(Stmt):
    def __init__(self, label: CellName) -> None:
        self.label = label

    def bf_code(self, pointer: Context) -> str:
        index = pointer.register_variable(self.label)

        code = ""
        code += TapeMove(TapeRefOffset(CELL_SIZE)).bf_code(pointer)
        code += TapePrefixRunin(TapeRefLabel("c/f"), TapeAdd(1)).bf_code(pointer)
        code += TapePrefixRunin(TapeRefLabel("c/t"), TapeZero()).bf_code(pointer)
        code += TapePrefixRunin(TapeRefLabel("c/i"), TapeZero()).bf_code(pointer)
        code += TapePrefixRunin(TapeRefLabel("c/i"), TapeAdd(index)).bf_code(pointer)

        return code

    def __str__(self) -> str:
        return f"cell.new {self.label}"


class CellMove(Stmt):
    def __init__(self, label: CellName) -> None:
        self.label = label

    def bf_code(self, pointer: Context) -> str:
        index = pointer.get_variable(self.label)
        current_index = pointer.cell_offset()

        search_direction = 1 if index > current_index else -1
        search_direction_rev = -1 if index > current_index else 1

        # Call on top, moved to top, update work1
        CHECK = [
            TapePrefixRunin(TapeRefLabel("c/w0"), TapeZero()),
            TapePrefixRunin(TapeRefLabel("c/w1"), TapeZero()),
            TapePrefixRunin(
                TapeRefLabel("c/i"),
                TapeCopy([TapeRefLabel("c/w0")], TapeRefLabel("c/w1")),
            ),
            TapePrefixRunin(TapeRefLabel("c/w1"), TapeAdd(1)),
            TapePrefixRunin(TapeRefLabel("c/w0"), TapeSub(index)),
            TapePrefixIfThen(
                TapeRefLabel("c/w0"), TapePrefixRunin(TapeRefLabel("c/w1"), TapeZero())
            ),
            TapePrefixIfThen(
                TapeRefLabel("c/w1"), TapePrefixRunin(TapeRefLabel("c/f"), TapeZero())
            ),
        ]

        code = ""

        code += CodeEmit("\nMove start\n").bf_code(pointer)
        code += CodeBlock(CHECK).bf_code(pointer)

        code += CodeEmit("\nLoop!\n").bf_code(pointer)
        code += TapePrefixLoop(
            TapeRefLabel("c/f"),
            CodeBlock(
                [
                    CodeEmit("\nmove\n"),
                    TapeMove(TapeRefOffset(search_direction * CELL_SIZE)),
                    CodeEmit("\ncheck\n"),
                    *CHECK,
                ]
            ),
        ).bf_code(pointer)
        code += CodeEmit("\nMove end\n").bf_code(pointer)

        return code

    def __str__(self) -> str:
        return f"cell.move {self.label}"


class CellSetType(Stmt):
    def __init__(self, value: int) -> None:
        self.value = value

    def bf_code(self, pointer: Context) -> str:
        code = ""
        code += TapePrefixRunin(TapeRefLabel("c/t"), TapeZero()).bf_code(pointer)
        code += TapePrefixRunin(TapeRefLabel("c/t"), TapeAdd(self.value)).bf_code(
            pointer
        )

        return code


class CellSetValue(Stmt):
    def __init__(self, value: int) -> None:
        self.value = value

    def bf_code(self, pointer: Context) -> str:
        code = ""
        code += TapePrefixRunin(TapeRefLabel("c/v"), TapeZero()).bf_code(pointer)
        code += TapePrefixRunin(TapeRefLabel("c/v"), TapeAdd(self.value)).bf_code(
            pointer
        )
        return code


class StackMachine(Transformer):
    def __init__(self) -> None:
        self.pointer = Context()

    # Primitive

    def int(self, tree):
        return int(tree[0])

    def p_offset(self, tree):
        return tree[0]

    def n_offset(self, tree):
        return -tree[0]

    # code
    def start(self, tree):
        return CodeBlock(tree)

    def cell_member(self, tree):
        return TapeRefLabel(tree[0])

    def tape_ref_label(self, tree):
        return tree[0]

    def stmt_blank(self, tree):
        return CodeEmit("")

    # tape prefix

    def stmt_tape_prefix_run_in(self, tree):
        offset, code = tree
        return TapePrefixRunin(offset, code)

    # code.xx
    def stmt_code_emit(self, tree):
        return CodeEmit(eval(tree[0]))

    # tape.xx

    def stmt_tape_copy(self, tree):
        dest_offsets = tree[:-1]
        trash_offset = tree[-1]

        return TapeCopy(dest_offsets, trash_offset)

    def stmt_tape_zero(self, tree):
        return TapeZero()

    def stmt_tape_add(self, tree):
        return TapeAdd(tree[0])

    # cell.xxx
    def stmt_cell_new(self, tree):
        return CellNew(tree[0])

    def stmt_cell_move(self, tree):
        return CellMove(tree[0])


def main():
    BASE_DIR = Path(__file__).resolve().parent
    EBNF_DIR = BASE_DIR / "ebnf"
    TEST_DIR = BASE_DIR / "test-src"

    with open(EBNF_DIR / "sm.ebnf") as f:
        sm_parser = Lark(f.read())

    with open(TEST_DIR / "a.bfc-sm") as f:
        src = f.read()

    tree = sm_parser.parse(src)
    print(tree.pretty())

    bf_code = StackMachine().transform(tree)
    print(bf_code)

    bf_code = bf_code.bf_code(Context())

    optimized = optimize(bf_code)

    print(f"Original: {len(bf_code)}")
    print(f"Optimized: {len(optimized)} ({len(bf_code) - len(optimized)} bytes saved)")

    print(optimized)


if __name__ == "__main__":
    main()
