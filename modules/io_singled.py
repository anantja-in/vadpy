import logging
import re
from datetime import timedelta

from vadpy.labels import Frame
from vadpy.module import GenericIOModuleBase
from vadpy.options import  Option

log = logging.getLogger(__name__)

class IOSingleD(GenericIOModuleBase):
    """Parse GT/VAD output Label files with decisions-only strings

    The format is:
    <time_from (in seconds)> <time_to (in seconds)> <decision (0|1)>
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

        frames = []

        previous_time_from = 0
        previous_time_to =   0

        with open(path) as f:
            for line in f:
                line = line.strip()
                if line == '':
                    continue

                match = self._reo.match(line)       # regex match

                if match:
                    # this values are expected
                    start = float(match.group(1))
                    end = float(match.group(2))
                    decision = bool(int(match.group(3)))

                    frame = Frame(start * self.k_factor,
                                      end * self.k_factor,
                                      decision,
                                      self.frame_len)

                    frames.append(frame)   # create new frame (above) and append it to frames list

        log.debug(('Parsed: {0}; Frames: {1}').format(path, len(frames)))
        return frames


    def write(self, labels, path):
        super(IOSingleD, self).write(labels, path)
        with open(path, 'w') as f:
            for frame in labels:
                f.write('{0}\t{1}\t{2}\n'.format(frame[0], frame[1], int(frame[2])) )
