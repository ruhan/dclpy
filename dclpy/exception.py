
class ViolationException(Exception):
    def __init__(self, fact, message="No message"):
        self.fact = fact
        code = '%s %s' % (fact['code'].co_filename, fact['code'].co_firstlineno)
        self.message = message + '\n' + code

class ConstraintDoesNotMatchException(Exception):
    pass

    
