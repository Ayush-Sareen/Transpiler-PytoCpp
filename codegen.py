def generate_cpp(ast):
    lines = ["#include <iostream>", "#include <string>", "using namespace std;"]
    main_lines = []

    def get_type(node):
        if node[0] == 'float':
            return 'float'
        elif node[0] == 'boolean':
            return 'bool'
        elif node[0] == 'number':
            return 'int'
        elif node[0] == 'string':
            return 'string'
        return 'auto'

    def gen(node, in_main=True):
        target = lines if not in_main else main_lines

        if node[0] == 'assign':
            var_name = node[1]
            value = gen(node[2])
            value_type = get_type(node[2])
            target.append(f"{value_type} {var_name} = {value};")

        elif node[0] == 'print':
            expr_type = get_type(node[1])
            value = gen(node[1])
            target.append(f"cout << {value} << endl;")

        elif node[0] == 'binop':
            left = gen(node[2])
            right = gen(node[3])
            return f"({left} {node[1]} {right})"

        elif node[0] == 'comparison':
            left = gen(node[2])
            right = gen(node[3])
            return f"{left} {node[1]} {right}"

        elif node[0] == 'logical':
            left = gen(node[2])
            right = gen(node[3])
            op = '&&' if node[1] == 'and' else '||'
            return f"{left} {op} {right}"

        elif node[0] == 'number':
            return str(node[1])

        elif node[0] == 'float':
            return str(node[1])

        elif node[0] == 'boolean':
            return "true" if node[1] else "false"

        elif node[0] == 'string':
            return f'"{node[1]}"'

        elif node[0] == 'id':
            return node[1]

        elif node[0] == 'if': 
            target.append(f"if ({gen(node[1])}) {{")
            for stmt in node[2]: 
                gen(stmt, in_main)
            target.append("}")

        elif node[0] == 'if_else':  
            target.append(f"if ({gen(node[1])}) {{")
            for stmt in node[2]:  # Inside if block
                gen(stmt, in_main)
            target.append("} else {")
            for stmt in node[3]:  # Inside else block
                gen(stmt, in_main)
            target.append("}")

        elif node[0] == 'for_range':
            var = node[1]
            start = 0 
            end = gen(node[2])
            target.append(f"for (int {var} = {start}; {var} < {end}; {var}++) {{")
            for stmt in node[3]:  # This is the list of statements inside the loop body
                gen(stmt, in_main)
            target.append("}")

    # Process the AST and generate the code
    for stmt in ast[1]:
        gen(stmt)

    lines.append("int main() {")
    lines.extend(main_lines)
    lines.append("return 0;\n}")

    return '\n'.join(lines)



