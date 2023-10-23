import ast


def extract_function_source(file_path, function_name):
    with open(file_path, "r", encoding="utf-8") as f:
        source = f.read()
        tree = ast.parse(source)

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name == function_name:
                start_line = node.lineno
                end_line = node.end_lineno
                return "\n".join(source.splitlines()[start_line - 1 : end_line])
    return None
