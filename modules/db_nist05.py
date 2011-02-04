import logging 
import os

from vadpy.module import DBModule
from vadpy.element import LITTLE_ENDIAN, FS_8000, BPS_16
from vadpy.options import Option

log = logging.getLogger(__name__)

class DBNIST05(DBModule):
    """NIST 2005 corpus module"""
    FLAGS       = LITTLE_ENDIAN | FS_8000 | BPS_16
                     
    def __init__(self, vadpy, options):
        super(DBNIST05, self).__init__(vadpy, options)
        self.source_dir = os.path.join(self.source_dir, self.dataset)

    def run(self):
        super(DBNIST05, self).run()
        elements = self.elements_from_dirs(self.source_name, 
                                           self.source_dir, 
                                           self.gt_dir, 
                                           self.FLAGS, 
                                           '^j.*')
        self.vadpy.pipeline.add(*elements)
