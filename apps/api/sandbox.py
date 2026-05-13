import ast

BLOCKED_NODES = (ast.Import, ast.ImportFrom)
BLOCKED_BUILTINS = {"eval", "exec", "open", "__import__", "compile", "breakpoint"}


def check_ast(code: str) -> str | None:
    """Returns an error message if code is unsafe, else None."""
    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        return f"Syntax error: {e}"

    for node in ast.walk(tree):
        if isinstance(node, BLOCKED_NODES):
            return "Import statements are not allowed."
        if isinstance(node, ast.Call):
            func = node.func
            name = None
            if isinstance(func, ast.Name):
                name = func.id
            elif isinstance(func, ast.Attribute):
                name = func.attr
            if name in BLOCKED_BUILTINS:
                return f"Use of '{name}' is not allowed."

    return None
