import logging 

from vadpy.module import Module
from vadpy.options import Option
from vadpy.element import * 

log = logging.getLogger(__name__)

class ModInfo(Module):
    """Prints known information about every element in the stream"""
    mode = Option()

    
    def __init__(self, vadpy, options):
        super(ModInfo, self).__init__(vadpy, options)

    def run(self):
        super(ModInfo, self).run()

        if self.mode == 'normal':            
            query = 'Source:\t\t{source_name}\n' \
                'Path:\t\t{source_path}\n' \
                'GT path:\t{gt_path}\n' \
                'GT labels:\t{gt_labels}\n' \
                'Vout path:\t{vout_path}\n' \
                'VAD labels:\t{vad_labels}\n' \
                'Length:\t\t{length} s.\n'
        
            for element in self.vadpy.pipeline:
                print(query.format(length = element.length, 
                                   **element.__dict__))

        elif self.mode == 'raw':
            for element in self.vadpy.pipeline:
                for attr in dir(element):
                    if not attr.startswith('__'):                        
                        print('{0:<20} {1}'.format(attr, getattr(element, attr)))
                print('\n')

