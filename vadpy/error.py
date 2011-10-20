class VADpyError(Exception):
    pass

class ModuleError(VADpyError):
    pass

class ModuleNotFoundError(VADpyError):
    def __init__(self, name):
        super(ModuleNotFoundError, self).__init__(
            'Module {0} could not be found'.format(name))

class ParseError(VADpyError):
    def __init__(self, message):
        super(ParseError, self).__init__(
            'Error parsing commands sequence: {0}'.format(message))

class MissingArgumentError(ParseError):
    def __init__(self, module, argument):
        super(ParseError, self).__init__(
            'Module {0} requires "{1}" argument'.format(module, argument))

