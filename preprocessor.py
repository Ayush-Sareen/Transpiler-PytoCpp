def preprocess_code(code: str) -> str:
    """
    Replaces Python-style indentation with C++-style braces.
    """
    lines = code.split('\n')
    result = []
    indent_stack = [0]

    for line in lines:
        if not line.strip():
            continue  # skip empty lines

        stripped = line.lstrip(' \t')  # FIXED: remove leading spaces/tabs
        indent = len(line) - len(stripped)

        if indent > indent_stack[-1]:
            result.append('{' + '\n' + stripped)
            indent_stack.append(indent)
        elif indent < indent_stack[-1]:
            while indent < indent_stack[-1]:
                result.append('}')
                indent_stack.pop()
            result.append(stripped)
        else:
            result.append(stripped)

    # Close remaining open blocks
    while len(indent_stack) > 1:
        result.append('}')
        indent_stack.pop()

    return '\n'.join(result)
