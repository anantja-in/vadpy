from vadpy.module import CompareModule
from vadpy.options import  Option
from vadpy.labels import equalize_framelen

from itertools import product
import logging 
log = logging.getLogger(__name__)

class ModFusionHistogram(CompareModule):
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

        vad_flags_combinations = product([0,1], repeat = len(self.inputs))
        for flags in vad_flags_combinations:
            speech_histogram[flags] = 0.0
            noise_histogram[flags] = 0.0
            lr_histogram[flags] = 0.0

        for element in self.vadpy.pipeline:            
            lo_list = []                        # labels object aka "lo"
            for attr in self.inputs:
                lo_list.append(getattr(element, attr))

            equalize_framelen(*(lo_list + [element.gt_labels]))
            frame_len = lo_list[0].frame_len
            frames_count = min(len(labels) for labels in lo_list)

            for i in range(0, frames_count):
                combined_frame = tuple(int(lo[i][2]) for lo in lo_list) # i-th frame, (start, end, --> speech <-- ) tuple
                
                if element.gt_labels[i][2]:
                    speech_histogram[combined_frame] += 1
                    speech_frames_count += 1
                else:                    
                    noise_histogram[combined_frame] += 1
                    noise_frames_count += 1

        # normalize histograms
        for key in speech_histogram:
            speech_histogram[key] /= speech_frames_count
            noise_histogram[key] /= noise_frames_count
            speech_val = speech_histogram[key]
            noise_val = noise_histogram[key]

            if noise_val == 0 and speech_val == 0:
                lr_histogram[key] = 0.0
            elif noise_val == 0:
                lr_histogram[key] = 1.0
            else:
                lr_histogram[key] = speech_val / noise_val
            

        print('Speech histogram:')
        for key in sorted(speech_histogram.keys()):
            print('{0:<25}{1:.3}'.format(key, speech_histogram[key]))

        print('\nNoise histogram:')
        for key in sorted(noise_histogram.keys()):
            print('{0:<25}{1:.3}'.format(key, noise_histogram[key]))

        print('\nLikelihood ratio histogram:')
        for key in sorted(lr_histogram.keys()):
            print('{0:<25}{1:.3}'.format(key, lr_histogram[key]))

