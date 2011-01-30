import collections

class Option(object):
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
        """Sets option's name and formats description"""
        if value:
            self.description = self.description.format(option = value)
        self._name = value


def bool_parser(value):
    return value.lower() not in ['', '""', "''", 'no', 'false']
