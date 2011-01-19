import logging 

from vadpy.module import Module
from vadpy.options import Option
from vadpy.element import * 

log = logging.getLogger(__name__)

class Info(Module):
    action = Option(default = 'show')
    query = Option(default = 'Source:\t\t{source}\nPath:\t\t{source_path}\nGT path:\t{gt_path}\nLength:\t\t{length} s.\n')
    
    def __init__(self, vadpy, options):
        super(Info, self).__init__(vadpy, options)

    def run(self):
        super(Info, self).run()

        if self.action == 'show':            
            # todo
            # print('Pipeline: ')
            # if element.flags ==  UNDEFINED:
            #     flags = 'Undefined'
            # else:
            #     if element.flags & LITTLE_ENDIAN:
            #         flags += 'Encoding: Little endian;'
            #     elif element.flags & BIG_ENDIAN:
            #         flags += 'Encoding: Big endian;'

            for element in self.vadpy.pipeline:
                query = self.query.format(source = element.source_name, 
                                          source_path = element.source_path, 
                                          gt_path = element.gt_path,
                                          length = element.length,)
                print(query)            
