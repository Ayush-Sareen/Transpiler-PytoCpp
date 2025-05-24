# Python to C++ Transpiler

This project is a simple Python-to-C++ transpiler implemented in Python. It reads Python-like code, processes it through multiple stages — preprocessing, lexical analysis, parsing, semantic checking — and finally generates equivalent C++ code.

Features:
- Converts Python indentation into C++-style curly braces
- Lexical analysis and parsing using PLY (Python Lex-Yacc)
- Semantic checks for undeclared variables and type compatibility
- Generates C++ code supporting variables, arithmetic, logical operations, if-else, for loops, and print statements

Project Files:
- codegen.py         -> Code generation (AST to C++)
- lexer.py           -> Lexer using PLY
- parser.py          -> Parser using PLY
- semantic.py        -> Semantic analyzer
- preprocessor.py    -> Converts indentation to braces
- sample.py          -> Sample Python input code
- output.cpp         -> Generated C++ output
- transpiler.py            -> Driver script that runs the entire pipeline
- parsetab.py        -> Auto-generated PLY table
- README.md          -> Project documentation

Installation:
1. Install Python 3.7 or higher
2. Install PLY:
   pip install ply

Usage:
1. Write your Python-style input code in sample.py
2. Run:
   python main.py
3. The transpiler will:
   - Preprocess the code (handle indentation)
   - Tokenize and parse the input
   - Perform semantic analysis
   - Generate and write the output C++ code to output.cpp
4. To compile and run:
   g++ output.cpp -o output
   ./output



Notes:
- Only basic Python features are supported
- Supports: int, float, bool, string types
- No support for functions, classes, lists, or other advanced constructs


References:
PLY (Python Lex-Yacc) - http://www.dabeaz.com/ply/
