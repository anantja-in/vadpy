import logging 
import os

from vadpy.module import DBModule
from vadpy.pipeline import LITTLE_ENDIAN, FS_8000, BPS_16
from vadpy.options import Option

log = logging.getLogger(__name__)

class DBNIST(DBModule):
    dataset = Option(default = "all")

    def __init__(self, vadpy, options):
        super(DBNIST, self).__init__(vadpy, options)

    def run(self):
        super(DBNIST, self).run()

        if self.dataset != "all":
            source_dir = os.path.join(self.source_dir, self.dataset)    
        else:
            source_dir = self.source_dir

        self.vadpy.pipeline.flags = LITTLE_ENDIAN | FS_8000 | BPS_16
        elements = self.elements_from_dirs('nist', source_dir, self.gt_dir)
                                           
        self.vadpy.pipeline.add(elements)
        log.debug('Added {0} elements to stream'.format(len(elements)))
