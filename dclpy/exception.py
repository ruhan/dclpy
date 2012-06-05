
class ViolationException(Exception):
    def __init__(self, fact, message="No message"):
        self.fact = fact
        self.message = message

class ConstraintDoesNotMatchException(Exception):
    pass

    