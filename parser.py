import ply.yacc as yacc
from lexer import tokens

precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('left', 'AND', 'OR'),
    ('left', 'EQEQ', 'NEQ', 'GT', 'LT', 'GEQ', 'LEQ')
)

def p_program(p):
    '''program : statement_list'''
    p[0] = ('program', p[1])

def p_statement_list(p):
    '''statement_list : statement
                      | statement_list statement'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

def p_block(p):
    '''block : statement
             | statement_list'''
    if isinstance(p[1], list):
        p[0] = p[1]
    else:
        p[0] = [p[1]]

def p_statement_assign(p):
    '''statement : ID EQUALS expr NEWLINE'''
    p[0] = ('assign', p[1], p[3])

def p_statement_print(p):
    '''statement : PRINT LPAREN expr RPAREN NEWLINE'''
    p[0] = ('print', p[3])

# Rule for handling 'if' statement
def p_statement_if(p):
    '''statement : IF expr COLON NEWLINE block'''
    p[0] = ('if', p[2], p[5])  # Simple if statement

# Rule for handling 'if-else' statement
def p_statement_if_else(p):
    '''statement : IF expr COLON NEWLINE block ELSE COLON NEWLINE block'''
    p[0] = ('if_else', p[2], p[5], p[9])  # if-else statement

def p_statement_for(p):
    '''statement : FOR ID IN RANGE LPAREN expr RPAREN COLON NEWLINE block'''
    p[0] = ('for_range', p[2], p[6], p[10])  # ('for_range', var, range_expr, block)

# Comparison operators
def p_expr_comparison(p):
    '''expr : expr EQEQ expr
            | expr NEQ expr
            | expr GT expr
            | expr LT expr
            | expr GEQ expr
            | expr LEQ expr'''
    p[0] = ('comparison', p[2], p[1], p[3])

# Logical operators
def p_expr_logical(p):
    '''expr : expr AND expr
            | expr OR expr'''
    p[0] = ('logical', p[2], p[1], p[3])

# Arithmetic operators
def p_expr_binop(p):
    '''expr : expr PLUS expr
            | expr MINUS expr
            | expr TIMES expr
            | expr DIVIDE expr'''
    p[0] = ('binop', p[2], p[1], p[3])

def p_expr_number(p):
    '''expr : NUMBER'''
    p[0] = ('number', p[1])

def p_expr_float(p):
    '''expr : FLOAT'''
    p[0] = ('float', p[1])

def p_expr_id(p):
    '''expr : ID'''
    p[0] = ('id', p[1])

def p_expr_string(p):
    '''expr : STRING'''
    p[0] = ('string', p[1][1:-1].encode().decode('unicode_escape'))  # Handle escape sequences in strings

def p_expr_true(p):
    '''expr : TRUE'''
    p[0] = ('boolean', True)

def p_expr_false(p):
    '''expr : FALSE'''
    p[0] = ('boolean', False)

# Parentheses handling
def p_expr_parens(p):
    '''expr : LPAREN expr RPAREN'''
    p[0] = p[2]

# Comma handling for expressions
def p_expr_comma(p):
    '''expr : expr COMMA expr'''
    p[0] = ('comma', p[1], p[3])

def p_error(p):
    if p is None:
        print("Syntax error at EOF")
    else:
        print(f"Syntax error at {p.value!r}")

parser = yacc.yacc()