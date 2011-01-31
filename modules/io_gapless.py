import logging 
import re

from vadpy.labels import Section
from vadpy.module import GenericIOModuleBase
from vadpy.options import  Option

log = logging.getLogger(__name__)

class IOGapless(GenericIOModuleBase):
    """Parse GT/VAD output Label files with decision labels in a gapless line format.

    The format is :
    <decision><decision>... 
    Example:
    111111000000000000001111111111111100011111
    """   
    def __init__(self, vadpy, options):
        super(IOGapless, self).__init__(vadpy, options)

    def run(self):
        super(IOGapless, self).run()
                
    def read(self, path):
        super(IOGapless, self).read(path)

        i = 0
        with open(path) as f:
            for line in f:
                if not line:
                    continue

                for char in line: 
                    decision = int(char)                    
                    section = Section(i * frame_len,
                                      (i + 1) * frame_len,
                                      decision, 
                                      self.frame_len)
                    sections.append(section)   # create new section (above) and append it to sections list

        log.debug(('Parsed: {0}; Sections: {1}').format(path, len(sections)))
        return sections


    def write(self, labels, path):
        super(IOGapless, self).write(labels, path)
        with open(path, 'w') as f:
            sout = ''.join(str(int(section[2])) for section in labels)
            f.write(sout)
    
