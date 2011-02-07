import logging 
import re
from datetime import timedelta

from vadpy.labels import Section
from vadpy.module import GenericIOModuleBase
from vadpy.options import  Option

log = logging.getLogger(__name__)

class IOSingleD(GenericIOModuleBase):
    """Parse GT/VAD output Label files with decisions-only strings

    The format is: 
    <time_from (in seconds)> <time_to (in seconds)> <decision (0|1) [<score>])
    """   
    k_factor = Option('k', parser = int)

    def __init__(self, vadpy, options):
        super(IOSingleD, self).__init__(vadpy, options)
        # regular expressions for parsing
        self._reo = re.compile(r'\s*([\d.,]+)\s*([\d.,]+)\s([-+\d\.]+)') 

    def run(self):
        super(IOSingleD, self).run()
                
    def read(self, path):
        super(IOSingleD, self).read(path)

        sections = []

        previous_time_from = 0
        previous_time_to =   0

        with open(path) as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue

                match = self._reo.match(line)       # regex match

                if match:
                    # this values are expected
                    start = float(match.group(1))
                    end = float(match.group(2))
                    decision = bool(int(match.group(3)))

                    section = Section(start * self.k_factor,
                                      end * self.k_factor,
                                      decision, 
                                      self.frame_len)

                    sections.append(section)   # create new section (above) and append it to sections list

        log.debug(('Parsed: {0}; Sections: {1}').format(path, len(sections)))
        return sections


    def write(self, labels, path):
        super(IOSingleD, self).write(labels, path)
        with open(path, 'w') as f:
            for section in labels:
                f.write('{0}\t{1}\t{2}\n'.format(section[0], section[1], int(section[2])) )
