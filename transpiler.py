from preprocessor import preprocess_code
from lexer import lexer
from parser import parser
from semantic import semantic_check
from codegen import generate_cpp

with open("sample.py", "r") as f:
    code = f.read()

# Step 1: Preprocess indentation
preprocessed_code = preprocess_code(code)
print("Preprocessed Code:\n", preprocessed_code)

if not preprocessed_code.endswith('\n'):
    preprocessed_code += '\n'

# Step 2: Lex + Parse
ast = parser.parse(preprocessed_code, lexer=lexer)

if ast is None:
    print("Parsing failed. No AST was generated.")
    exit(1)

# Step 3: Semantic Analysis
semantic_check(ast)
print("AST generated:", ast)

# Step 4: Code Generation
cpp_code = generate_cpp(ast)

# Step 5: Output
with open("output.cpp", "w") as out:
    out.write(cpp_code)

print("\nC++ code written to output.cpp")