from . import parser
import sys
src = sys.argv[1]

print(src)
print(parser.parser(src).parse())
