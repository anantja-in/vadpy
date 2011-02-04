import logging 
import os

from vadpy.module import DBModule
from vadpy.element import BIG_ENDIAN, FS_8000, BPS_16
from vadpy.options import Option

log = logging.getLogger(__name__)

class DBAURORA(DBModule):
    """AURORA2z corpus module"""
    FLAGS       = BIG_ENDIAN | FS_8000 | BPS_16
                     
    def __init__(self, vadpy, options):
        super(DBAURORA, self).__init__(vadpy, options)

    def run(self):
        super(DBAURORA, self).run()
        elements = self.elements_from_dirs(self.source_name, 
                                           self.source_dir, 
                                           self.gt_dir, 
                                           self.FLAGS)
        self.vadpy.pipeline.add(*elements)
