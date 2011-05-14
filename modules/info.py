import logging 
import time

from vadpy.module import Module
from vadpy.options import Option, split_parser
from vadpy.element import * 

log = logging.getLogger(__name__)

class ModInfo(Module):
    """Prints known information about every element in the stream

    The special values for attr option are:
    __raw__     Print all elements attributes' values
    __info__    Print formatted output of common attributes
    __summary__ Print summary of the pipeline
    """
    attributes = Option('attr', split_parser, 
                        'Raw element\'s attributes to print')
    
    def __init__(self, vadpy, options):
        super(ModInfo, self).__init__(vadpy, options)

    def run(self):
        super(ModInfo, self).run()
        pipeline = self.vadpy.pipeline

        if not self.attributes:
            return
        elif '__info__' in self.attributes:
            query = ('Source:\t\t{source_name}\n'
                     'Path:\t\t{source_path}\n' 
                     'GT path:\t{gt_path}\n' 
                     'GT labels:\t{gt_labels}\n'
                     'Vout path:\t{vout_path}\n'
                     'VAD labels:\t{vad_labels}\n'
                     'Length:\t\t{length} s.\n')
        
            for element in pipeline:
                print(query.format(length = element.length, 
                                   **element.__dict__))
        elif '__raw__' in self.attributes:
            for element in pipeline:
                for attr in dir(element):
                    if not attr.startswith('__'):
                        print('{0:<20}{1}'.format(attr, getattr(element, attr)))

        elif '__summary__' in self.attributes:
            sum_length_sec = sum(elem.length for elem in pipeline)
            hrs = int(sum_length_sec // 3600)
            sum_length_sec -= hrs * 3600
            mins = int(sum_length_sec // 60)
            sum_length_sec -= mins*60
            secs = int(sum_length_sec)

            print(('Pipeline information:\n'
                   'Elements count: {0}\n'
                   'Total length: {h} h. {m} min. {s} sec.').format(len(pipeline), 
                                                                    h = hrs, 
                                                                    m = mins, 
                                                                    s = secs))                  
        else:
            for element in pipeline:
                for attr in self.attributes:
                    print('{0:<20}{1}'.format(attr, getattr(element, attr)))
