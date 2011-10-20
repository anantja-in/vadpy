import collections
from .error import VADpyError

class Option(object):
    """VADpy module's option class"""
    def __init__(self,
                 name = None,
                 parser = str,
                 description = '',):
        """
        name        - Option's name, (if empty, it's then automatically set by ModuleMetaClass)
        parser      - Callable parser (function or type) that parses option's value
        description - Option's description
        """
        self.description = description
        self.parser = parser
        self.name = name                # if None, will be set from attribute name by ModuleMetaClass
        self.module = None              # set by ModuleMetaclass

    def parse(self, value):
        value = self.parser(value)
        return value

    @property
    def name(self):
        """Option's name"""
        return self._name

    @name.setter
    def name(self, value):
        """Sets option name"""
        self._name = value


class StrictOption(Option):
    """VADpy module's strict option class

    An error is rased if option's value is not in 'values' list
    """
    def __init__(self,
                 name = None,
                 parser = str,
                 values = [],
                 description = '', ):
        """
        values      - a list of possible values
        """
        self._values = values
        super(StrictOption, self).__init__(name, parser, description)

    def parse(self, value):
        parsed_value = self.parser(value)
        if isinstance(parsed_value, collections.Iterable):
            if len(set(parsed_value) - set(self._values)) != 0:
                raise OptionValueError(parsed_value)
        else:
            if parsed_value not in self._values:
                raise OptionValueError(parsed_value)
        return parsed_value

def bool_parser(value):
    value = value.lower()
    if value in ['', '""', "''", 'no', 'false']:
        return False
    elif value in ['true', 'yes']:
        return True
    else:
        raise VADpyError('What kind of boolean do you think "{0}" is?'.format(value))

def split_parser(value):
    if value == '':
        return []
    return value.split(',')

def odd_parser(value):
    value = int(value)
    if value % 2 == 0:
        raise VADpyError('{0} is not an odd number'.format(value))
    return value

class OptionValueError(Exception):
    def __init__(self, value):
        super(OptionValueError, self).__init__("Incorrect option's value: {0}".format(value))
