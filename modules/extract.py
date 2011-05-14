import io
import os 

from vadpy.labels import Frame, Labels
from vadpy.module import MonotonicPipelineModule
from vadpy.options import  Option, StrictOption, bool_parser
from vadpy.element import Element, UNDEFINED

import logging 
log = logging.getLogger(__name__)

SEEK_CUR = 1 # io.SEEK_CUR is new in Python 2.7

class ModExtract(MonotonicPipelineModule):
    """Extracts the GT-based data from files (without adding a new element to the stream)
    
    ModExtract is used for extracting speech / noise data separately
    """
    out_path = Option('out-path',
                      description = 'Optput file path, to which the extracted data will be written')
    mode = StrictOption(parser = lambda s: s.lower()[0], values = ['s', 'n'],
                        description = 'Indicates whether speech or noise shoud be extracted (speech/noise)')

    def __init__(self, vadpy, options):
        super(ModExtract, self).__init__(vadpy, options)

    def run(self):
        super(ModExtract, self).run()
        pipeline = self.vadpy.pipeline

        for element in pipeline:
            source_io = io.FileIO(element.source_path)
            out_io = io.FileIO(self.format_path(self.out_path, **element.format_args), 'w')

            frame_size = element.gt_labels.frame_len * element.fs * (element.bps / 8)
            assert frame_size.is_integer(), 'Extraction shifting size must be an integer number. Try changing the frame length'
            frame_size = int(frame_size)
                        
            for label in element.gt_labels:
                speech_flag = label[2]
                if (speech_flag and self.mode == 's' or 
                    not speech_flag and self.mode == 'n'):
                    data = source_io.read(frame_size)
                    out_io.write(data)
                else:
                    source_io.seek(frame_size, SEEK_CUR)
                    
            source_io.close()
            out_io.close() 
