#######################################
# INTERPRETER
#######################################

from runtime import RTResult
from tokens import TT_PLUS, TT_MINUS, TT_MUL, TT_DIV
from values import Number



class Interpreter:
    def visit(self, node, context):
        method_name = f"visit_{type(node).__name__}"
        method = getattr(self, method_name)
        return method(node, context)

    def no_visit_method(self, node, context):
        raise Exception(f"Kono visit_{type(node).__name__} defined kora nei")

    def visit_NumberNode(self, node, context):
        return RTResult().success(
            Number(node.tok.value).set_context(context).set_pos(node.pos_start, node.pos_end)
        )

    # Number(node.tok.value).set_pos(node.pos_start, node.pos_end)

    def visit_BinOpNode(self, node, context):

        res = RTResult()
        left = res.register(self.visit(node.left_node, context))
        if res.error:
            return res
        right = res.register(self.visit(node.right_node, context))

        if node.op_tok.type == TT_PLUS:
            result, error = left.added_to(right)
        elif node.op_tok.type == TT_MINUS:
            result, error = left.subbed_by(right)
        elif node.op_tok.type == TT_MUL:
            result, error = left.multed_by(right)
        elif node.op_tok.type == TT_DIV:
            result, error = left.dived_by(right)

        if error:
            return res.failure(error)
        else:
            return res.success(result.set_pos(node.pos_start, node.pos_end))

    def visit_UnaryOpNode(self, node, context):
        res = RTResult()
        number = res.register(self.visit(node.node, context))
        if res.error:
            return res

        error = None
        if node.op_tok.type == TT_MINUS:
            number, error = number.multed_by(Number(-1))

        if error:
            return res.failure(error)

        else:
            return res.success(number.set_pos(node.pos_start, node.pos_end))
