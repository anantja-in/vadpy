import logging 
import re
from datetime import timedelta

from vadpy.data import Section, Data
from vadpy.module import IOModule
from vadpy.options import  Option

log = logging.getLogger(__name__)

class IOCat(IOModule):
    """Concatenates all elements' data and GT into one element"""   


    def __init__(self, vadpy, options):
        super(IOCat, self).__init__(vadpy, options)


    def run(self):
        super(IOCat, self).run()
       
        if self.action == 'read':
            for element in self.vadpy.pipeline:
                element.gt_data =  Data(self.read(element.gt_path), self.frame_len)

        elif self.action == 'write':
            for element in self.vadpy.pipeline:
                self.write(element.gt_data, element.gt_path + '.x')

                
    def read(self, path):
        log.debug(('Parsing: {0}').format(path))

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


    def write(self, data, path):
        # with open(path, 'w') as f:
        #     for section in data:
        #         f.write('{0}\t{1}\t{2}\n'.format(section[0], section[1], int(section[2])))
        pass
