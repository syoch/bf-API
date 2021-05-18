from .asm import table
from .label import getLabel

def compile(ast):
    instructions = []

    for stmt in ast:
        if type(stmt) == list:
            instructions += table["loop1"]
            instructions += compile(stmt)
            instructions += table["loop2"]
        if stmt == "+":
            instructions += ["pop", "inc", "push"]
        elif stmt == "-":
            instructions += ["pop", "dec", "push"]
        elif stmt == "<":
            instructions += ["ins"]
        elif stmt == ">":
            instructions += ["des"]
        elif stmt == ".":
            instructions += ["put"]
        elif stmt == ",":
            instructions += ["get"]
    return instructions
