#######################################
# RUN
#######################################


from context import Context
from interpreter import Interpreter
from lexer import Lexer
from parser import Parser
from symbolTable import SymbolTable
from values import Number

global_symbol_table = SymbolTable()
global_symbol_table.set("null", Number(0))

def run(fn, text):
    # Generate tokens
    lexer = Lexer(fn, text)
    tokens, error = lexer.make_tokens()
    if error:
        return None, error

    # Generate AST
    parser = Parser(tokens)
    ast = parser.parse()
    if ast.error:
        return None, ast.error

    # Run program
    interpreter = Interpreter()
    context = Context("<AjobFile>")
    context.symbol_table = global_symbol_table
    result = interpreter.visit(ast.node, context)  # This returns an RTResult object
    if result.error:
        return None, result.error

    return result.value, None
