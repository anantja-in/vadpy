import logging 
import os

from vadpy.module import DBModule
from vadpy.element import LITTLE_ENDIAN, FS_8000, BPS_16
from vadpy.options import Option

log = logging.getLogger(__name__)

class DBNIST05(DBModule):
    """NIST 2005 corpus module"""
    SOURCE_NAME = 'NIST05'
    FLAGS       = LITTLE_ENDIAN | FS_8000 | BPS_16

    dataset = Option(description = 'The dataset (directory name in source-dir) to be used. Leave blank for reading files from source-dir',
                     default = '')

    def __init__(self, vadpy, options):
        super(DBNIST05, self).__init__(vadpy, options)

    def run(self):
        super(DBNIST05, self).run()
        source_dir = os.path.join(self.source_dir, self.dataset)

        elements = self.elements_from_dirs(self.SOURCE_NAME, source_dir, self.gt_dir, self.FLAGS)
        self.vadpy.pipeline.add(*elements)
        log.debug('Added {0} elements to stream'.format(len(elements)))


