from . import parser
from . import compile
import sys
src = sys.argv[1]

print(compile.compile(parser.parser(src).parse()))
