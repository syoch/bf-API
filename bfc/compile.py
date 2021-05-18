from .asm import table


def compile(ast):
    instructions = []

    for stmt in ast:
        if type(stmt) == list:
            raise NotImplementedError()
        if stmt == "+":
            instructions += table["inc"]
        elif stmt == "-":
            instructions += table["dec"]
        elif stmt == "<":
            instructions += table["lef"]
        elif stmt == ">":
            instructions += table["rig"]
        elif stmt == ".":
            instructions += table["put"]
        elif stmt == ",":
            instructions += table["get"]
    return instructions
