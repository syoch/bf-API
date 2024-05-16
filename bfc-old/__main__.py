from typing import List
from .parser import parser
from .compile import compile as pseudo
from .asm import convert as platform
from .pseudo.optimize import auto as optimizer


def compile(src: str) -> List[str]:
    ast = parser(src).parse()
    pseudocode = pseudo(ast)
    optimizedcode = optimizer(pseudocode)
    platformcode = platform(optimizedcode)
    return platformcode


def main():
    import sys
    src = sys.argv[1]
    for line in compile(src):
        print(line)


if __name__ == "__main__":
    main()
