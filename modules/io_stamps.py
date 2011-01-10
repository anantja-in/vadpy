import logging 
import re
from datetime import timedelta

from vadpy.data import Section, Data, extend_sections
from vadpy.module import Option, IOModule

log = logging.getLogger(__name__)

class IOStamps(IOModule):
    """Parse GT/VAD files with positive decisions-only strings

    The format is: 
    # voiced section: 
    <time_from (datetime stamp regex)><splitter><time_to (datetime stamp regex)>
    
    Where stamp regular expression may look like:
    '(?P<dd>\d+):(?P<hh>\d+):(?P<mm>\d+):(?P<ss>\d+):(?P<ms>\d+)' # dd:hh:mm:ss:ms

    Or any other shorter version:
    (?P<mm>\d+):(?P<ss>\d+) # mm:ss

    The names of the groups are ones from the list below:
    dd - days         1x86400s
    hh - hours        1x3600s
    mm - minutes      1x60s
    ss - seconds      1x1s
    ms - milliseconds 1x0.001s 
    mk - microseconds 1xe-6s
    """
    res = Option('re')
    splitstr = Option('split')

    def __init__(self, vadpy, options):
        super(IOStamps, self).__init__(vadpy, options)
        self._reo = re.compile(self.res)


    def run(self):
        super(IOStamps, self).run()
        
        if self.action == 'read':
            for element in self.vadpy.pipeline:
                element.gt_data =  Data(
                    extend_sections(element, self.read(element.gt_path), self.frame_len),
                    self.frame_len)

        elif self.action == 'write':
            for element in self.vadpy.pipeline:
                self.write(element.gt_data, element.gt_path + '.amr1')
               
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

                # split line, perform regex match
                stamp_from, stamp_to = line.split(self.splitstr)
                time_from = self._get_seconds(stamp_from)
                time_to = self._get_seconds(stamp_to)


                if previous_time_to >= time_from: # overlapping sections:
                    time_from = previous_time_to
                else:
                    # create unvoiced sections
                    if previous_time_to != time_from:
                        usection = Section(previous_time_to, time_from, False, self.frame_len)
                        sections.append(usection)

                # create voiced section
                if time_from != time_to:
                    vsection = Section(time_from, time_to, True, self.frame_len)
                    sections.append(vsection)

                previous_time_from = time_from
                previous_time_to = time_to

        log.debug(('Parsed: {0}; Sections: {1}').format(path, len(sections)))
        return sections


    def write(self, data, path):
        with open(path, 'w') as f:
            start_section = None
            previos_section = None # (i-1_th section)

            for section in data:                
                if not start_section: # first processed section
                    voiced = section.voiced
                    start_section = section

                if start_section.voiced != section.voiced: # sections differ
                    if not section.voiced:                 # start_section is voiced                        
                        f.write('{0} {1}\n'.format(start_section.start, previos_section.end))
                    else: 
                        start_section = section

                previos_section = section             
       



    def _get_seconds(self, stamp):
        match = self._reo.match(stamp) # re match
        
        seconds = 0

        for period_name, value in match.groupdict().items():
            value = float(value) # convert string to float
            if period_name == 'ss': # seconds
                seconds += value
            elif period_name == 'mm': # minutes
                seconds += 60*value
            elif period_name == 'hh': # hours
                seconds += 3600*value
            elif period_name == 'ms': # milliseconds
                seconds += 0.001*value
            elif period_name == 'mk': # microseconds
                seconds += 0.000001*value
            elif period_name == 'dd': # days
                seconds += 86400*value
            else:
                raise ValueError('Wrong period name: "{0}"'.format(period_name))

        return seconds
