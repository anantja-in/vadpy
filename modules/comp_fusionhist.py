from vadpy.module import ComputeModule
from vadpy.options import  Option
from vadpy.labels import equalize_framelen

from itertools import product
import math

import logging 
log = logging.getLogger(__name__)

COMB_MIN_VALUE = 1.0

class ModFusionHistogram(ComputeModule):
    """Fusion histogram calculator"""
    def __init__(self, vadpy, options):
        super(ModFusionHistogram, self).__init__(vadpy, options)

    def run(self):
        super(ModFusionHistogram, self).run()
        speech_frames_count = 0.0
        noise_frames_count = 0.0

        # initialize histograms
        speech_histogram = {}
        noise_histogram = {}
        lr_histogram = {}
        probabilites = {}

        vad_combinations = product([0,1], repeat = len(self.inputs))
        for comb_vec in vad_combinations:
            speech_histogram[comb_vec] = COMB_MIN_VALUE
            noise_histogram[comb_vec] = COMB_MIN_VALUE
            lr_histogram[comb_vec] = COMB_MIN_VALUE
            probabilites[comb_vec] = COMB_MIN_VALUE

        for element in self.vadpy.pipeline:            
            lo_list = []                        # labels object aka "lo"
            for attr in self.inputs:
                lo_list.append(getattr(element, attr))

            equalize_framelen(*(lo_list + [element.gt_labels]))
            frame_len = lo_list[0].frame_len
            frames_count = min(len(labels) for labels in lo_list)

            for i in range(0, frames_count):
                # i-th frame, (start, end, --> speech <-- ) tuple
                comb_vec = tuple(int(lo[i][2]) for lo in lo_list) 
                
                probabilites[comb_vec] += 1
                if element.gt_labels[i][2]:
                    speech_histogram[comb_vec] += 1
                    speech_frames_count += 1
                else:                    
                    noise_histogram[comb_vec] += 1
                    noise_frames_count += 1
                
        # normalize histograms
        for key in probabilites:
            speech_histogram[key] /= speech_frames_count
            noise_histogram[key] /= noise_frames_count
            probabilites[key] /= (speech_frames_count + noise_frames_count)

            speech_val = speech_histogram[key]
            noise_val = noise_histogram[key]

            if noise_val == 0 or speech_val == 0:
                lr_histogram[key] = 0.0
            elif noise_val == 0:
                lr_histogram[key] = 1.0
            else:
                lr_histogram[key] = math.log(speech_val / noise_val)
                
        # update pipeline with histogram data
        self.add_result('speech', speech_histogram)
        self.add_result('noise', noise_histogram)
        self.add_result('lr', lr_histogram)
        self.add_result('p', probabilites)

    def _format_results(self):
        res = self._get_results()
        speech_histogram = res.speech
        noise_histogram = res.noise
        lr_histogram = res.lr
        p = res.p

        combinations = sorted(p.keys())
        s = 'Speech histogram:\n'
        for key in combinations:
            s += '{0:<25}{1:.3}\n'.format(key, speech_histogram[key])
            
        s += '\nNoise histogram:\n'
        for key in combinations:
            s += '{0:<25}{1:.3}\n'.format(key, noise_histogram[key])

        s += '\nLog likelihood ratio histogram:\n'
        for key in combinations:
            s += '{0:<25}{1:.3}\n'.format(key, lr_histogram[key])

        s += '\nProbabilities:\n'
        for key in combinations:
            s += '{0:<25}{1:.3}\n'.format(key, p[key])
            
        return s
