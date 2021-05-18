def compile(ast):
    for stmt in ast:
        if type(stmt) == list:
            raise NotImplementedError()
