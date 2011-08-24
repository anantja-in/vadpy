import io
import os
import operator
from functools import reduce

from vadpy.module import Module
from vadpy.options import  Option, split_parser, odd_parser
from vadpy.labels import Frame, Labels

import logging 
log = logging.getLogger(__name__)

MAJORITY_METHOD = 'majority'
SIMPLE_HIST_METHOD = 'simplehist'
BAYES_METHOD = 'bayes'

class ModFusion(Module):
    """The majority voting/histogram fusion module   
    """
    inputs = Option(parser = split_parser, 
                    description =  "VAD labels attributes separated by comma")
    output = Option(description = 'Output labels attribute')
    max_diff_rate = Option('max-diff-rate', float, 
                           ('Maximum difference rate of labels frame count.\n'
                            'Recommented value: 0.005 (0.5%)'))
    margs = Option(parser = split_parser, description = 'Method arguments')
    method = Option(parser = str.lower, description = 'Fusion method')
    ctx_size = Option('ctx-size', int,  'Temporal context size')


    def __init__(self, vadpy, options):
        super(ModFusion, self).__init__(vadpy, options)

        if self.method == MAJORITY_METHOD:
            assert self.inputs >= 3 and len(self.inputs) % 2 == 1, \
                'Labels attributes number is even or is less than 3'
        elif self.method == BAYES_METHOD:
            self._sr_attr = self.margs[0] # speech to nonspeech attribute name
        elif self.method == SIMPLE_HIST_METHOD:
            pass
        else:
            raise Exception('Invalid fusion method: {0}'.format(self.method))
        

    def run(self):
        super(ModFusion, self).run()

        use_histogram = hasattr(self.vadpy.pipeline, 'modfusionhistogram')
        use_bayes = hasattr(self.vadpy.pipeline, 'modsr') and use_histogram
        
        if self.method == SIMPLE_HIST_METHOD:
            assert use_histogram, ('Simple histogram method was selected, '
                                   'but histogram was not provided')
        elif self.method == BAYES_METHOD:
            assert use_bayes, ('Simple histogram method was selected, but '
                               'histogram or speech to non-speech ratio was '
                               'not provided')
        
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
                raise Exception(("Labels objects' difference ({0}) is "
                                 "greater than max-diff-rate ({1})").format(
                        max_len - min_len, 
                        min_len * self.max_diff_rate))

            frames_count = min_len
            frame_len = lo_list[0].frame_len
            frames = []        
            for i in range(0, frames_count):

                comb_matrix = []
                for j in range(max(0, i - self.ctx_size), 
                               min(i + self.ctx_size + 1, frames_count)):
                    comb_matrix.append(tuple(
                            int(lo[j][2]) for lo in lo_list))
                                                                    
                if self.method == BAYES_METHOD:
                    decision = self._bayes_method(comb_matrix)
                elif self.method == SIMPLE_HIST_METHOD:
                    decision = self._simple_histogram_method(comb_matrix)
                else: # simple majority / temporal context
                    decision = self._majority_method(comb_matrix)

                frames.append(Frame(i * frame_len, 
                                    (i + 1) * frame_len,                                  
                                    decision, 
                                    frame_len))

            lo_combined = Labels(frames, frame_len)
            setattr(element, self.output, lo_combined)


    def _majority_method(self, comb_matrix):        
        speech_count = 0
        noise_count = 0
        for column in comb_matrix:
            for value in column:
                if value:
                    speech_count += 1
                else:
                    noise_count += 1

        return speech_count > noise_count 

    def _simple_histogram_method(self, comb_matrix):
        lr = self.vadpy.pipeline.modfusionhistogram.lr # likelihood ratio
        # decision
        return (reduce(operator.mul, 
                       (lr[column_vec] for column_vec in comb_matrix)) 
                >= 1)
        
    def _bayes_method(self, comb_matrix):
        histogram = self.vadpy.pipeline.modfusionhistogram
        lr = histogram.lr # likelihood ratio
        sr = self.vadpy.pipeline.modsr.sr[self._sr_attr]
        return (reduce(operator.mul, 
                       (lr[column_vec] for column_vec in comb_matrix))
                >= 1 / sr)
