"""Package core shim: expose `run(fn, text)` and `global_symbol_table`.

This module composes the modular lexer, parser, interpreter and builtins
and exposes the small public API expected by external scripts.
"""

from .lexer import Lexer
from .parser import Parser
from .interpreter import Interpreter, Context, SymbolTable
from .builtins import populate_symbol_table


global_symbol_table = SymbolTable()
populate_symbol_table(global_symbol_table)


def run(fn, text):
    lexer = Lexer(fn, text)
    tokens, error = lexer.make_tokens()
    if error:
        return None, error

    parser = Parser(tokens)
    ast = parser.parse()
    if ast.error:
        return None, ast.error

    interpreter = Interpreter()
    context = Context("<program>")
    context.symbol_table = global_symbol_table
    result = interpreter.visit(ast.node, context)

    return result.value, result.error
