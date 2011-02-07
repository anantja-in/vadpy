import logging 
import os

from vadpy import element
from vadpy.module import DBModule
from vadpy.options import Option, split_parser

log = logging.getLogger(__name__)


FLAGS = {'undefined' : element.UNDEFINED,
         'le' : element.LITTLE_ENDIAN,
         'be' : element.BIG_ENDIAN,
         '8000hz' : element.FS_8000,
         '16bps' : element.BPS_16,
         }


class DBQUICK(DBModule):
    """A 'quick' generic database module (extends DBModule via flags option)

    Flags:
    le      - Little endian encoding
    be      - Big endian encoding
    8000hz  - Data framerate is 8000hz 
    16bps   - 16 bits per frame
    """
    flags = Option(parser = split_parser, description = 'Flags describing data in the database. ')
    re = Option(description = 'Reqular expression filter')

    def __init__(self, vadpy, options):
        super(DBQUICK, self).__init__(vadpy, options)
        flags = element.UNDEFINED

        for flag in self.flags:
            try:
                flags |= FLAGS[flag]
            except KeyError:
                raise Exception('Flag {0} cannot be found'.format(val))
        self.flags = flags

    def run(self):
        super(DBQUICK, self).run()
        elements = self.elements_from_dirs(self.source_name, 
                                           self.source_dir, 
                                           self.gt_dir, 
                                           self.flags, 
                                           self.re)
        self.vadpy.pipeline.add(*elements)
