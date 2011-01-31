import logging 
import os
import re

from vadpy.module import DBModule
from vadpy.element import Element, LITTLE_ENDIAN, FS_8000, BPS_16
from vadpy.options import Option
from vadpy  import common

log = logging.getLogger(__name__)

class DBNIST08(DBModule):
    """NIST 2008 corpus module"""
    SOURCE_NAME  = 'NIST08'
    FLAGS        = LITTLE_ENDIAN | FS_8000 | BPS_16     # database flags
    CHANNELS     = [1, 2, 3, 5, 7, 8, 9, 12, 13]
    DATAUNITS_RE = [
        r'^20070313_145145.*',]
                          
    dataset = Option(description = 'The dataset (directory name in source-dir) to be used. ' \
                                   'Leave blank for reading files from source-dir',)                     
    dataunits = Option(description = 'The data units\' numbers to be processed. ' \
                                     'Leave blank to process all units. Example: {option}=1,2,3', )                       
    channels = Option(description = 'Audio channels\' numbers (files) to be processed. ' \
                                    'Leave blank to process all channels. Example: {option}=2,9,12')
                      
    def __init__(self, vadpy, options):
        super(DBNIST08, self).__init__(vadpy, options)

    def run(self):
        super(DBNIST08, self).run()
        self._parse_options()

        elements = self._get_elements()
        self.vadpy.pipeline.add(*elements)
        log.debug('Added {0} elements to stream'.format(len(elements)))

    def _parse_options(self):
        if self.dataunits:
            self.dataunits = list(int(index) - 1 for index in self.dataunits.split(','))
        else:
            self.dataunits = range(0, len(self.DATAUNITS_RE)) # artificial indices list
        
        if self.channels:
            self.channels = list(int(channel) for channel in self.channels.split(','))
        else:
            self.channels = self.CHANNELS

    def _get_elements(self):
        elements = []
        source_dir = os.path.join(self.source_dir, self.dataset)

        for index in self.dataunits:
            # get single dataunit files
            source_files = common.listdir(source_dir, self.DATAUNITS_RE[index])
            gt_file = common.listdir(self.gt_dir, self.DATAUNITS_RE[index])[0] # there should be a single GT file here
            # compare GT file name and Data file name without "_CHxx" ending
            assert gt_file == source_files[0][:-5], "GT file's and Data file's name mismatch: {0}".format(gt_file) 

            # sort out the channels
            source_files = (fname for fname in source_files 
                            if int(fname[-2:]) in self.channels)
            for source_file in source_files:                
                elements.append(
                    Element(self.SOURCE_NAME, 
                            os.path.abspath( os.path.join(source_dir, source_file)),
                            os.path.abspath( os.path.join(self.gt_dir, gt_file)),
                            self.FLAGS)
                    )
            return elements
