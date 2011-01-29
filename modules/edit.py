import logging 

from vadpy.module import Module
from vadpy.options import Option

log = logging.getLogger(__name__)


class ModEdit(Module):
    """The ModEdit module allows editing elements' attributes.
    
    Attribute vlaue formatting:
    {{elem}}           - element. 
    {{elem.attrubute}} - element's attribute value 
    {{attr}}           - element's attribute original value (attr option)    
    """
    attr = Option(description = 'Attribute to be edited')
    value = Option(description = "New value to be set (see module's description")

    def __init__(self, vadpy, options):
        super(ModEdit, self).__init__(vadpy, options)

    def run(self):
        super(ModEdit, self).run()        
        if not self.attr:
            return 

        for element in self.vadpy.pipeline:
            old_val = getattr(element, self.attr)
            new_val = self.value.format(attr = old_val, 
                                        elem = element)
            setattr(element, attr, new_val)
        
