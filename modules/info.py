import logging 

from vadpy.module import Module
from vadpy.options import Option
from vadpy.element import * 

log = logging.getLogger(__name__)

class ModInfo(Module):
    """Prints known information about every element in the stream"""
    action = Option()

    
    def __init__(self, vadpy, options):
        super(ModInfo, self).__init__(vadpy, options)

    def run(self):
        super(ModInfo, self).run()

        query = 'Source:\t\t{source_name}\n' \
            'Path:\t\t{source_path}\n' \
            'GT path:\t{gt_path}\n' \
            'GT labels:\t{gt_labels}\n' \
            'Vout path:\t{vout_path}\n' \
            'VAD labels:\t{vad_labels}\n' \
            'Length:\t\t{_length} s.\n'
        
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
                print(query.format(**element.__dict__))

