import os
import math
from .values import RTResult, Number, String, List, BaseFunction
from .errors import RTError


class BuiltInFunction(BaseFunction):
    def __init__(self, name):
        super().__init__(name)

    def execute(self, args):
        res = RTResult()
        exec_ctx = self.generate_new_context()

        method_name = f"execute_{self.name}"
        method = getattr(self, method_name, None)

        res.register(self.check_and_populate_args(
            method.arg_names if method else [], args, exec_ctx))
        if res.should_return():
            return res

        if not method:
            return res.failure(RTError(self.pos_start, self.pos_end, f"No execute_{self.name} method defined", exec_ctx))

        return_value = res.register(method(exec_ctx))
        if res.should_return():
            return res
        return res.success(return_value)

    def copy(self):
        copy = BuiltInFunction(self.name)
        copy.set_context(self.context)
        copy.set_pos(self.pos_start, self.pos_end)
        return copy

    def __repr__(self):
        return f"<built-in function {self.name}>"

    #################################

    def execute_print(self, exec_ctx):
        print(str(exec_ctx.symbol_table.get("value")))
        return RTResult().success(Number(0))

    execute_print.arg_names = ["value"]

    def execute_print_ret(self, exec_ctx):
        return RTResult().success(String(str(exec_ctx.symbol_table.get("value"))))

    execute_print_ret.arg_names = ["value"]

    def execute_input(self, exec_ctx):
        try:
            text = input()
        except EOFError:
            text = ""
        return RTResult().success(String(text))

    execute_input.arg_names = []

    def execute_input_int(self, exec_ctx):
        while True:
            try:
                text = input()
            except EOFError:
                return RTResult().success(Number(0))
            try:
                number = int(text)
                break
            except ValueError:
                print(f"'{text}' must be an integer. Try again!")
        return RTResult().success(Number(number))

    execute_input_int.arg_names = []

    def execute_clear(self, exec_ctx):
        os.system("cls" if os.name == "nt" else "clear")
        return RTResult().success(Number(0))

    execute_clear.arg_names = []

    def execute_is_number(self, exec_ctx):
        is_number = isinstance(exec_ctx.symbol_table.get("value"), Number)
        return RTResult().success(Number(1 if is_number else 0))

    execute_is_number.arg_names = ["value"]

    def execute_is_string(self, exec_ctx):
        is_string = isinstance(exec_ctx.symbol_table.get("value"), String)
        return RTResult().success(Number(1 if is_string else 0))

    execute_is_string.arg_names = ["value"]

    def execute_is_list(self, exec_ctx):
        is_list = isinstance(exec_ctx.symbol_table.get("value"), List)
        return RTResult().success(Number(1 if is_list else 0))

    execute_is_list.arg_names = ["value"]

    def execute_is_function(self, exec_ctx):
        is_function = isinstance(
            exec_ctx.symbol_table.get("value"), BaseFunction)
        return RTResult().success(Number(1 if is_function else 0))

    execute_is_function.arg_names = ["value"]

    def execute_append(self, exec_ctx):
        list_ = exec_ctx.symbol_table.get("list")
        value = exec_ctx.symbol_table.get("value")

        if not isinstance(list_, List):
            return RTResult().failure(RTError(self.pos_start, self.pos_end, "First argument must be list", exec_ctx))

        list_.elements.append(value)
        return RTResult().success(Number(0))

    execute_append.arg_names = ["list", "value"]

    def execute_pop(self, exec_ctx):
        list_ = exec_ctx.symbol_table.get("list")
        index = exec_ctx.symbol_table.get("index")

        if not isinstance(list_, List):
            return RTResult().failure(RTError(self.pos_start, self.pos_end, "First argument must be list", exec_ctx))

        if not isinstance(index, Number):
            return RTResult().failure(RTError(self.pos_start, self.pos_end, "Second argument must be number", exec_ctx))

        try:
            element = list_.elements.pop(index.value)
        except Exception:
            return RTResult().failure(RTError(self.pos_start, self.pos_end, "Element at this index could not be removed from list because index is out of bounds", exec_ctx))
        return RTResult().success(element)

    execute_pop.arg_names = ["list", "index"]

    def execute_extend(self, exec_ctx):
        listA = exec_ctx.symbol_table.get("listA")
        listB = exec_ctx.symbol_table.get("listB")

        if not isinstance(listA, List):
            return RTResult().failure(RTError(self.pos_start, self.pos_end, "First argument must be list", exec_ctx))

        if not isinstance(listB, List):
            return RTResult().failure(RTError(self.pos_start, self.pos_end, "Second argument must be list", exec_ctx))

        listA.elements.extend(listB.elements)
        return RTResult().success(Number(0))

    execute_extend.arg_names = ["listA", "listB"]

    def execute_len(self, exec_ctx):
        list_ = exec_ctx.symbol_table.get("list")
        if not isinstance(list_, List):
            return RTResult().failure(RTError(self.pos_start, self.pos_end, "Argument must be list", exec_ctx))
        return RTResult().success(Number(len(list_.elements)))

    execute_len.arg_names = ["list"]

    def execute_math_modulo(self, exec_ctx):
        num = exec_ctx.symbol_table.get("num")
        mod = exec_ctx.symbol_table.get("mod")
        if not isinstance(num, Number):
            return RTResult().failure(RTError(self.pos_start, self.pos_end, "First argument must be number", exec_ctx))
        if not isinstance(mod, Number):
            return RTResult().failure(RTError(self.pos_start, self.pos_end, "Second argument must be number", exec_ctx))
        return RTResult().success(Number(num.value % mod.value))

    execute_math_modulo.arg_names = ["num", "mod"]

    def execute_math_floor(self, exec_ctx):
        num = exec_ctx.symbol_table.get("num")
        if not isinstance(num, Number):
            return RTResult().failure(RTError(self.pos_start, self.pos_end, "Argument must be number", exec_ctx))
        return RTResult().success(Number(math.floor(num.value)))

    execute_math_floor.arg_names = ["num"]

    def execute_math_ceil(self, exec_ctx):
        num = exec_ctx.symbol_table.get("num")
        if not isinstance(num, Number):
            return RTResult().failure(RTError(self.pos_start, self.pos_end, "Argument must be number", exec_ctx))
        return RTResult().success(Number(math.ceil(num.value)))

    execute_math_ceil.arg_names = ["num"]

    def execute_math_round(self, exec_ctx):
        num = exec_ctx.symbol_table.get("num")
        if not isinstance(num, Number):
            return RTResult().failure(RTError(self.pos_start, self.pos_end, "Argument must be number", exec_ctx))
        return RTResult().success(Number(round(num.value)))

    execute_math_round.arg_names = ["num"]

    def execute_math_abs(self, exec_ctx):
        num = exec_ctx.symbol_table.get("num")
        if not isinstance(num, Number):
            return RTResult().failure(RTError(self.pos_start, self.pos_end, "Argument must be number", exec_ctx))
        return RTResult().success(Number(abs(num.value)))

    execute_math_abs.arg_names = ["num"]

    def execute_math_sqrt(self, exec_ctx):
        num = exec_ctx.symbol_table.get("num")
        if not isinstance(num, Number):
            return RTResult().failure(RTError(self.pos_start, self.pos_end, "Argument must be number", exec_ctx))
        return RTResult().success(Number(math.sqrt(num.value)))

    execute_math_sqrt.arg_names = ["num"]

    def execute_math_sin(self, exec_ctx):
        num = exec_ctx.symbol_table.get("num")
        if not isinstance(num, Number):
            return RTResult().failure(RTError(self.pos_start, self.pos_end, "Argument must be number", exec_ctx))
        return RTResult().success(Number(math.sin(num.value)))

    execute_math_sin.arg_names = ["num"]

    def execute_math_cos(self, exec_ctx):
        num = exec_ctx.symbol_table.get("num")
        if not isinstance(num, Number):
            return RTResult().failure(RTError(self.pos_start, self.pos_end, "Argument must be number", exec_ctx))
        return RTResult().success(Number(math.cos(num.value)))

    execute_math_cos.arg_names = ["num"]

    def execute_math_tan(self, exec_ctx):
        num = exec_ctx.symbol_table.get("num")
        if not isinstance(num, Number):
            return RTResult().failure(RTError(self.pos_start, self.pos_end, "Argument must be number", exec_ctx))
        return RTResult().success(Number(math.tan(num.value)))

    execute_math_tan.arg_names = ["num"]

    def execute_math_pow(self, exec_ctx):
        num = exec_ctx.symbol_table.get("num")
        power = exec_ctx.symbol_table.get("power")
        if not isinstance(num, Number):
            return RTResult().failure(RTError(self.pos_start, self.pos_end, "First argument must be number", exec_ctx))
        if not isinstance(power, Number):
            return RTResult().failure(RTError(self.pos_start, self.pos_end, "Second argument must be number", exec_ctx))
        return RTResult().success(Number(num.value**power.value))

    execute_math_pow.arg_names = ["num", "power"]

    def execute_run(self, exec_ctx):
        fn = exec_ctx.symbol_table.get("fn")
        if not isinstance(fn, String):
            return RTResult().failure(RTError(self.pos_start, self.pos_end, "Argument must be string", exec_ctx))

        fn = fn.value

        try:
            with open(fn, "r") as f:
                script = f.read()
        except Exception as e:
            return RTResult().failure(RTError(self.pos_start, self.pos_end, f"Failed to load script \"{fn}\"\n" + str(e), exec_ctx))

        # import run lazily to avoid circular imports during module load
        from .core import run

        _, error = run(fn, script)
        if error:
            return RTResult().failure(RTError(self.pos_start, self.pos_end, f"Failed to finish executing script \"{fn}\"\n" + error.as_string(), exec_ctx))

        return RTResult().success(Number(0))

    execute_run.arg_names = ["fn"]


def populate_symbol_table(symbol_table):
    # constants
    symbol_table.set("khali", Number(0))
    symbol_table.set("bhul", Number(0))
    symbol_table.set("thik", Number(1))
    symbol_table.set("onko_pi", Number(math.pi))
    symbol_table.set("onko_e", Number(math.e))

    # builtins
    symbol_table.set("bol", BuiltInFunction("print"))
    symbol_table.set("likhey_bol", BuiltInFunction("print_ret"))
    symbol_table.set("jigesh_kor", BuiltInFunction("input"))
    symbol_table.set("sonkha_jigesh_kor", BuiltInFunction("input_int"))
    symbol_table.set("porishkar", BuiltInFunction("clear"))
    symbol_table.set("sonkha_ki", BuiltInFunction("is_number"))
    symbol_table.set("kotha_ki", BuiltInFunction("is_string"))
    symbol_table.set("list_ki", BuiltInFunction("is_list"))
    symbol_table.set("kaaj_ki", BuiltInFunction("is_function"))
    symbol_table.set("laga", BuiltInFunction("append"))
    symbol_table.set("byass_ber_kor", BuiltInFunction("pop"))
    symbol_table.set("atka", BuiltInFunction("extend"))
    symbol_table.set("lomba", BuiltInFunction("len"))
    symbol_table.set("modulo", BuiltInFunction("math_modulo"))
    symbol_table.set("floor", BuiltInFunction("math_floor"))
    symbol_table.set("ceil", BuiltInFunction("math_ceil"))
    symbol_table.set("round", BuiltInFunction("math_round"))
    symbol_table.set("abs", BuiltInFunction("math_abs"))
    symbol_table.set("sqroot", BuiltInFunction("math_sqrt"))
    symbol_table.set("sin", BuiltInFunction("math_sin"))
    symbol_table.set("cos", BuiltInFunction("math_cos"))
    symbol_table.set("tan", BuiltInFunction("math_tan"))
    symbol_table.set("pow", BuiltInFunction("math_pow"))
    symbol_table.set("Maach", BuiltInFunction("run"))
