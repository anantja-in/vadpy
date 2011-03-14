import logging 
import re
from datetime import timedelta

from vadpy.labels import Frame
from vadpy.module import Option, GenericIOModuleBase

log = logging.getLogger(__name__)

class IOStamps(GenericIOModuleBase):
    """Parse GT/VAD files with positive decisions-only strings

    The format is: 
    # voiced frame: 
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
               
    def read(self, path):
        super(IOStamps, self).read(path)
        frames = []

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

                if previous_time_to >= time_to:
                    log.warning('Skipping frame: {0}-{1}'.format(time_from, time_to))
                    continue

                if previous_time_to >= time_from: # overlapping frames:
                    time_from = previous_time_to
                else:
                    # create unvoiced frames
                    if previous_time_to != time_from:
                        uframe = Frame(previous_time_to, time_from, False, self.frame_len)
                        frames.append(uframe)

                # create voiced frame
                if time_from != time_to:
                    vframe = Frame(time_from, time_to, True, self.frame_len)
                    frames.append(vframe)

                previous_time_from = time_from
                previous_time_to = time_to

        log.debug(('Parsed: {0}; Frames: {1}').format(path, len(frames)))
        return frames


    def write(self, labels, path):
        super(IOStamps, self).write(labels, path)
        with open(path, 'w') as f:
            begin_frame = None
            previos_frame = None # (i-1_th frame)

            try:
                # although it's expected that labels.frames contain
                # consequtevely changing frames (voiced/unvoiced/voiced/unvoiced/...)
                # we can still insure ourselves against several consequtive voiced or unvoiced frames.
                segment_start = labels.frames[0]
                
                for frame in labels.frames:
                    if segment_start.voiced != frame.voiced: # frames differ
                        if not frame.voiced:                 # segment_start....previous_frame segment is voiced
                            f.write('{0} {1}\n'.format(segment_start.start, previos_frame.end))
                        segment_start = frame
                    previos_frame = frame

                if segment_start.voiced: # finalize
                    f.write('{0} {1}\n'.format(segment_start.start, previos_frame.end))
                    
            except IndexError:
                pass

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
