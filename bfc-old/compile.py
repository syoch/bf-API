from .label import getLabel


def compile(ast):
    instructions = []

    for stmt in ast:
        if type(stmt) == list:
            label = getLabel()
            instructions += [f"{label}:"]
            instructions += compile(stmt)
            instructions += ["peek", f"jnz {label}"]
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
