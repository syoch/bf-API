# Memory layout
# +---+---+---+---+
# | 0 | 1 | 2 | 3 |
# +---+---+---+---+
#
# 0: Special
# 1: Work
# 2: Index
# 3: Value
#
# Function Memory layout
#   +---------------+
#   | Special 0xFF  |
#   +---------------+
#   | Argument count|
#   +---------------+
#   |  Arguments... |
#   +---------------+
#   |Local Variables|
#   +---------------+