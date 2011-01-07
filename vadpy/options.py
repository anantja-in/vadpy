class Option(object):
    def __init__(self, 
                 name = None,
                 description = '', 
                 parse_type = str, 
                 parse_func = None,
                 default = None):
        """

        default - default value (string, as if recieved from command-line)
        """
        self.name = name    # if None, will be set from attribute name
        self.module = None  # set by ModuleMetaclass 
        self.description = description
        self.parse_type = parse_type
        self.parse_func = parse_func
        self.default = default

    def parse(self, value):
        value = self.parse_type(value) # type conversion
        
        if self.parse_func and hasattr(self.parse_func, '__call__'):
            value = self.parse_func(value)
        return value
