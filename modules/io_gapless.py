import logging
import re

from vadpy.labels import Frame
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
        frames = []
        with open(path) as f:
            for line in f:
                line = line.strip()
                if len(line) == 0:
                    continue

                for char in line:
                    decision = int(char)
                    frame = Frame(i * self.frame_len,
                                      (i + 1) * self.frame_len,
                                      decision,
                                      self.frame_len)
                    frames.append(frame)   # create new frame (above) and append it to frames list
                    i+= 1
        log.debug(('Parsed: {0}; Frames: {1}').format(path, len(frames)))
        return frames


    def write(self, labels, path):
        super(IOGapless, self).write(labels, path)
        with open(path, 'w') as f:
            sout = ''.join(str(int(frame[2])) for frame in labels)
            f.write(sout)

