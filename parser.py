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
    '''block : LBRACE statement_list RBRACE
             | LBRACE RBRACE'''
    if len(p) == 4:
        p[0] = p[2]
    else:
        p[0] = []

def p_statement_assign(p):
    '''statement : ID EQUALS expr'''
    p[0] = ('assign', p[1], p[3])

def p_statement_print(p):
    '''statement : PRINT LPAREN expr RPAREN'''
    p[0] = ('print', p[3])

def p_statement_if(p):
    '''statement : IF expr COLON block'''
    p[0] = ('if', p[2], p[4])

def p_statement_if_else(p):
    '''statement : IF expr COLON block ELSE COLON block'''
    p[0] = ('if_else', p[2], p[4], p[7])

def p_statement_for(p):
    '''statement : FOR ID IN RANGE LPAREN expr RPAREN COLON block'''
    p[0] = ('for_range', p[2], p[6], p[9])

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
    # Handle escape sequences in strings
    p[0] = ('string', p[1][1:-1].encode().decode('unicode_escape'))

def p_expr_true(p):
    '''expr : TRUE'''
    p[0] = ('boolean', True)

def p_expr_false(p):
    '''expr : FALSE'''
    p[0] = ('boolean', False)

def p_expr_parens(p):
    '''expr : LPAREN expr RPAREN'''
    p[0] = p[2]

def p_expr_comma(p):
    '''expr : expr COMMA expr'''
    p[0] = ('comma', p[1], p[3])

def p_error(p):
    if p is None:
        print("Syntax error at EOF")
    else:
        print(f"Syntax error at {p.value!r}")

parser = yacc.yacc()
