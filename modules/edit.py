import os
import logging 

from vadpy.module import Module
from vadpy.options import Option

log = logging.getLogger(__name__)


class ModEdit(Module):
    """The ModEdit module allows editing elements' attributes.
    
    Additional formatting arguments for value option:
    {attr}    - element's attribute original value (attr option)
    {fname}   - file name (if value is a path)
    {fdir}    - file's directory (if value is a path)    
    """
    attr = Option(description = 'Attribute to be edited')
    value = Option(description = "New value to be set (see module's description")
    from_attr = Option(description = 'Attribute from which a value should be copied')
    to_attr = Option(description = 'Attribute to which a value should be copied')

    def __init__(self, vadpy, options):
        super(ModEdit, self).__init__(vadpy, options)

    def run(self):
        super(ModEdit, self).run()                
        if self.attr:
            for element in self.vadpy.pipeline:
                try:
                    old_val = getattr(element, self.attr)
                except AttributeError:
                    old_val = ''

                fdir = ''
                fname = ''
                fdir, fname = os.path.split(old_val)
                new_val = self.format_path(self.value, 
                                           attr = old_val, 
                                           fname = fname, 
                                           fdir = fdir, 
                                           **element.format_args)
                setattr(element, self.attr, new_val)        
        if self.from_attr:
            for element in self.vadpy.pipeline:
                val = getattr(element, self.from_attr)
                setattr(element, self.to_attr, val)
