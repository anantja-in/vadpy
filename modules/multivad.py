import io
import os

from vadpy.module import Module
from vadpy.options import  Option, bool_parser, split_parser
from vadpy.labels import Frame, Labels

import logging 
log = logging.getLogger(__name__)

class ModMultiVAD(Module):
    """The MultiVAD module accepts odd number of VAD Labels objects and outputs combined labels
    
    The combination rule is max out of all, that's why an odd number of VAD Labels objects are required
    """
    labels_attr = Option('labels-attr', split_parser, "VAD labels attributes separated by comma")
    out_labels_attr = Option('out-labels-attr', description = 'Output labels attribute')
    max_diff_rate = Option('max-diff-rate', float, 'Maximum difference rate of labels frame count.\n' \
                                                    'Recommented value: 0.005 (0.5%)')

    def __init__(self, vadpy, options):
        super(ModMultiVAD, self).__init__(vadpy, options)
        assert self.labels_attr >= 3 and len(self.labels_attr) % 2 == 1, \
              'Labels attributes number is even or is less than 3'

    def run(self):
        super(ModMultiVAD, self).run()        
        
        for element in self.vadpy.pipeline:    
            lo_list = [] # labels object
            for attr in self.labels_attr:
                lo_list.append(getattr(element, attr))                
            lo_count = len(lo_list)            
            min_flen = min(lo.frame_len for lo in lo_list)
            for lo in lo_list:
                lo.frame_len = min_flen
                
            min_len = min(len(lo) for lo in lo_list)
            max_len = max(len(lo) for lo in lo_list)
            if (max_len - min_len > min_len * self.max_diff_rate):
                raise Exception("Labels objects' difference ({0}) is greater than max-diff-rate ({1})".format(
                        max_len - min_len, 
                        min_len * self.max_diff_rate))
            
            frames = []        
            frame_len = lo_list[0].frame_len
            frames_count = min_len

            for i in range(0, frames_count):
                combined_frame = []
                for lo in lo_list:
                    combined_frame.append(lo[i][2]) # i-th frame, (start, end, --> voiced <-- ) tuple

                voiced_count = len([value for value in combined_frame 
                                    if value])
                unvoiced_count = lo_count - voiced_count                

                decision = voiced_count > unvoiced_count and True or False
                frames.append(Frame(i * frame_len, 
                                        (i + 1) * frame_len,                                  
                                        decision, 
                                        frame_len))
            
            lo_combined = Labels(frames, frame_len)

            setattr(element, self.out_labels_attr, lo_combined)
