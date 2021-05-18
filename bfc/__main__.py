from . import parser
from . import compile
from . import asm
import sys
src = sys.argv[1]

print(asm.convert(compile.compile(parser.parser(src).parse())))
