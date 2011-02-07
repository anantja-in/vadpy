import logging 
import os

from vadpy import common
from vadpy.module import DBModule
from vadpy.element import Element, BIG_ENDIAN, FS_8000, BPS_16
from vadpy.options import Option, split_parser

log = logging.getLogger(__name__)

class DBAURORA(DBModule):
    """AURORA2z corpus module"""    
    env = Option(parser = split_parser, description = 'Environment numbers separated by ","')
    snr = Option(parser = split_parser, description = 'SNR rates separated by ","')

    FLAGS       = BIG_ENDIAN | FS_8000 | BPS_16
    
    def __init__(self, vadpy, options):
        super(DBAURORA, self).__init__(vadpy, options)
        
    def run(self):
        super(DBAURORA, self).run()
        elements = []
        for env in self.env:
            for snr in self.snr:                             
                source_file_name = 'N{0}_SNR{1}'.format(env, snr)
                source_file_path = os.path.join(self.source_dir, source_file_name)

                if self.dataset == 'TRAIN' :
                    gt_file_path = os.path.join(self.gt_dir, source_file_name)
                elif self.dataset == 'TEST':
                    gt_file_path = os.path.join(self.gt_dir, 'N{0}'.format(env))

                elements.append(
                    Element(self.source_name,
                            source_file_path, 
                            gt_file_path,
                            self.FLAGS)
                    )
        self.vadpy.pipeline.add(*elements)
