def compile(ast):
    for stmt in ast:
        if type(stmt) == list:
            raise NotImplementedError()
        if stmt == "+":
            print("inc")
        elif stmt == "-":
            print("dec")
        elif stmt == "<":
            print("lef")
        elif stmt == ">":
            print("rig")
        elif stmt == ".":
            print("put")
        elif stmt == ",":
            print("get")
