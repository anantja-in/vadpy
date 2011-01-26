import logging 

from vadpy.module import Module
from vadpy.options import Option

log = logging.getLogger(__name__)


class Edit(Module):
    """The Edit module allows editing elements's arguments in template-formatting way. 

    The available arguments are Module.format_args and 
    {srcname}     element's source name
    {srcpath}     element's source data's path
    {gtpath}      element's GT path
    """
    source_name = Option('source-name', default = '{srcname}')
    source_path = Option('source-path', default = '{srcpath}')
    gt_path = Option('gt-path', default = '{gtpath}')

    def __init__(self, vadpy, options):
        super(Edit, self).__init__(vadpy, options)

    def run(self):
        super(Edit, self).run()
        
        for element in self.vadpy.pipeline:
            element.source_name =  self.source_name.format(srcname = element.source_name, **self.format_args)
            element.source_path = self.source_path.format(srcpath = element.source_path, **self.format_args)
            element.gt_path = self.gt_path.format(gtpath = element.gt_path, **self.format_args)                
        
