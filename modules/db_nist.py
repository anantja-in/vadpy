import logging 
import os

from vadpy.module import DBModule
from vadpy.element import LITTLE_ENDIAN, FS_8000, BPS_16
from vadpy.options import Option

log = logging.getLogger(__name__)

class DBNIST(DBModule):
    """NIST 2005 corpus module"""
    dataset = Option(description = 'The dataset (directory name in source-dir) to be used. Leave blank for reading files from source-dir',
                     default = '')

    def __init__(self, vadpy, options):
        super(DBNIST, self).__init__(vadpy, options)

    def run(self):
        super(DBNIST, self).run()

        if self.dataset:
            source_dir = os.path.join(self.source_dir, self.dataset)
        else:
            source_dir = self.source_dir

        flags = LITTLE_ENDIAN | FS_8000 | BPS_16

        elements = self.elements_from_dirs('nist', source_dir, self.gt_dir, flags)

        self.vadpy.pipeline.add(*elements)
        log.debug('Added {0} elements to stream'.format(len(elements)))
