#######################################
# VALUES
#######################################

from errors import RTError

class Number:
    def __init__(self, value):
        self.value = value
        self.set_pos()
        self.set_context()

    def set_pos(self, pos_start=None, pos_end=None):
        self.pos_start = pos_start
        self.pos_end = pos_end
        return self  # Ensure the method returns the current instance.

    def set_context(self, context=None):
        self.contex = context
        return self

    def added_to(self, other):
        if isinstance(other, Number):
            return Number(self.value + other.value).set_context(self.contex), None

    def subbed_by(self, other):
        if isinstance(other, Number):
            return Number(self.value - other.value).set_context(self.contex), None

    def multed_by(self, other):
        if isinstance(other, Number):
            return Number(self.value * other.value).set_context(self.contex), None

    def dived_by(self, other):
        if isinstance(other, Number):
            if other.value == 0:
                return None, RTError(
                    other.pos_start,
                    other.pos_end,
                    "Kono BKL e hobe je 0 diye kono number ke divide kore",
                    self.contex
                )  # Handle division by zero case.
            return Number(self.value / other.value).set_context(self.contex), None

    def __repr__(self):
        return str(self.value)
