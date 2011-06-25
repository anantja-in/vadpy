import io
import os

from vadpy.module import Module
from vadpy.options import  Option, split_parser, odd_parser
from vadpy.labels import Frame, Labels

import logging 
log = logging.getLogger(__name__)

MAJORITY_METHOD = 'majority'

class ModFusion(Module):
    """The Fusion module accepts odd number of VAD Labels objects and outputs combined labels
    
    The combination rule is max out of all, that's why an odd number of VAD Labels objects are required
    """
    inputs = Option(parser = split_parser, description =  "VAD labels attributes separated by comma")
    output = Option(description = 'Output labels attribute')
    max_diff_rate = Option('max-diff-rate', float, 'Maximum difference rate of labels frame count.\n' \
                                                    'Recommented value: 0.005 (0.5%)')
    margs = Option(parser = split_parser, description = 'Method arguments')
    method = Option(parser = str.lower, description = 'Fusion method')

    def __init__(self, vadpy, options):
        super(ModFusion, self).__init__(vadpy, options)

        if self.method == MAJORITY_METHOD:
            assert self.inputs >= 3 and len(self.inputs) % 2 == 1, \
                'Labels attributes number is even or is less than 3'
            self._tmp_ctx_size = int(self.margs[0]) # temporal context size
        else:
            raise Exception('Invalid fusion method: {0}'.format(self.method))
        

    def run(self):
        super(ModFusion, self).run()
        
        for element in self.vadpy.pipeline:    
            lo_list = [] # labels object
            for attr in self.inputs:
                lo_list.append(getattr(element, attr))

            min_flen = min(lo.frame_len for lo in lo_list)
            for lo in lo_list:
                lo.frame_len = min_flen
                
            min_len = min(len(lo) for lo in lo_list)
            max_len = max(len(lo) for lo in lo_list)
            if (max_len - min_len > min_len * self.max_diff_rate):
                raise Exception("Labels objects' difference ({0}) is greater than max-diff-rate ({1})".format(
                        max_len - min_len, 
                        min_len * self.max_diff_rate))

            frames_count = min_len
            if self.method == MAJORITY_METHOD:                
                self._majority(element, lo_list, frames_count)


    def _majority(self, element, lo_list, frames_count):
        frames = []        
        frame_len = lo_list[0].frame_len

        use_histogram = hasattr(self.vadpy.pipeline, 'modfusionhistogram')

        for i in range(0, frames_count):
            combined_frames = []
            combined_labels = []
            for j in range(max(0, i - self._tmp_ctx_size), 
                           min(i + self._tmp_ctx_size + 1, frames_count)):
                frame_labels = []
                for lo in lo_list:
                    # j-th frame, (start, end, --> speech <-- ) tuple
                    frame_labels.append(int(lo[j][2])) 
                    combined_labels.append(lo[j][2])
                combined_frames.append(tuple(frame_labels))
                

            decision = None
            if use_histogram:
                histogram = self.vadpy.pipeline.modfusionhistogram
                lr = histogram.lr # likelihood ratio
                speech_count = 0
                sum_lr = 0
                for cframes in combined_frames:                    
                    sum_lr += lr[cframes]

                decision = sum_lr >= 0

            else: # simple majority / temporal context
                speech_count = len([value for value in combined_labels 
                                    if value])
                noise_count = len(lo_list) - speech_count                
                decision = speech_count > noise_count 

            assert decision != None, 'Decision has not been made!'
            frames.append(Frame(i * frame_len, 
                                (i + 1) * frame_len,                                  
                                decision, 
                                frame_len))

        lo_combined = Labels(frames, frame_len)
        setattr(element, self.output, lo_combined)
