#######################################
# RUNTIME RESULT
#######################################


class RTResult:
    def __init__(self):
        self.value = None
        self.error = None

    def register(self, res):
        if isinstance(res, RTResult):
            if res.error:
                self.error = res.error
            return res.value
        return res

    def success(self, value):
        self.value = value
        return self

    def failure(self, error):
        self.error = error
        return self
