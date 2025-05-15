def semantic_check(ast):
    declared = {}
    functions = {}

    def check_node(node):
        if node[0] == 'assign':
            var_name = node[1]
            value_type = get_type(node[2])
            declared[var_name] = value_type  # Register the variable as declared
            check_node(node[2])  # Also check RHS expression
        
        elif node[0] == 'id':
            var_name = node[1]
            if var_name not in declared:
                raise Exception(f"Semantic Error: '{var_name}' used before assignment")

        elif node[0] == 'binop':
            check_node(node[2])
            check_node(node[3])
            left_type = get_type(node[2])
            right_type = get_type(node[3])
            if left_type != right_type:
                raise Exception(f"Semantic Error: Incompatible types for binary operation {node[1]}: '{left_type}' and '{right_type}'")
            if node[1] in ['+', '-', '*', '/']:
                if left_type not in ['int', 'float'] or right_type not in ['int', 'float']:
                    raise Exception(f"Semantic Error: Arithmetic operations require numeric operands.")
            return left_type

        elif node[0] == 'logical':
            check_node(node[2])
            check_node(node[3])
            left_type = get_type(node[2])
            right_type = get_type(node[3])
            if left_type != 'bool' or right_type != 'bool':
                raise Exception(f"Semantic Error: Logical operations require 'bool' operands.")
            return 'bool'

        elif node[0] == 'comparison':
            check_node(node[2])
            check_node(node[3])
            return 'bool'  # Comparisons always return 'bool'

        elif node[0] == 'print':
            check_node(node[1])
            value_type = get_type(node[1])
            if value_type not in ['int', 'float', 'bool', 'string']:
                raise Exception(f"Semantic Error: Unsupported type '{value_type}' for print statement.")

        elif node[0] == 'if_else':
            check_node(node[1])  # condition
            for stmt in node[2]:
                check_node(stmt)  # true branch
            for stmt in node[3]:
                check_node(stmt)  # false branch

        elif node[0] == 'func_def':
            func_name = node[1]
            if func_name in functions:
                raise Exception(f"Semantic Error: Function '{func_name}' already defined.")
            functions[func_name] = node[2]  # Store function and its body
            for stmt in node[2]:
                check_node(stmt)

        elif node[0] == 'func_call':
            func_name = node[1]
            if func_name not in functions:
                raise Exception(f"Semantic Error: Function '{func_name}' not defined.")
            # Add argument matching logic here if needed

    def get_type(node):
        nodetype = node[0]
        if nodetype == 'number':
            return 'int'
        elif nodetype == 'float':
            return 'float'
        elif nodetype == 'boolean':
            return 'bool'
        elif nodetype == 'string':
            return 'string'
        elif nodetype == 'id':
            return declared.get(node[1], 'unknown')
        elif nodetype == 'binop':
            left_type = get_type(node[2])
            right_type = get_type(node[3])
            if 'float' in (left_type, right_type):
                return 'float'
            elif 'int' in (left_type, right_type):
                return 'int'
            return 'unknown'
        elif nodetype == 'comparison':
            return 'bool'
        elif nodetype == 'logical':
            return 'bool'
        else:
            raise Exception(f"Error: Unrecognized value node: {node}")

    # Start semantic check for all statements in the AST
    for stmt in ast[1]:
        check_node(stmt)