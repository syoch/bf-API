from typing import List
from .parser import parser
from .compile import compile as pseudo
from .asm import convert as platform


def compile(src: str) -> List[str]:
    ast = parser(src).parse()
    pseudocode = pseudo(ast)
    platformcode = platform(pseudocode)
    return platformcode


def main():
    import sys
    src = sys.argv[1]
    print(compile(src))


if __name__ == "__main__":
    main()
