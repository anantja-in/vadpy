import logging 

from vadpy.module import Module
from vadpy.options import Option

log = logging.getLogger(__name__)


class Source(Module):
    info = Option(default = '')
    name = Option(default = '{source}')

    def __init__(self, vadpy, options):
        super(Source, self).__init__(vadpy, options)

    def run(self):
        super(Source, self).run()
        
        for element in self.vadpy.pipeline:
            element.source_name =  self.srcname.format(name = element.source_name)
            
            if self.info:
                self.info.format(source = element.source_name, 
                                 source_path = element.source_path, 
                                 gt_path = element.gt_path,
                                 length = element.length)
                
        
