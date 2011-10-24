from vadpy.module import ComputeModule
from vadpy.options import  Option
from vadpy.labels import equalize_framelen

from itertools import product
from copy import deepcopy
import math

import logging
log = logging.getLogger(__name__)

COMB_MIN_VALUE = 1.0

class ModSourceHistogram(ComputeModule):
    """Source-based histogram calculator"""
    def __init__(self, vadpy, options):
        super(ModSourceHistogram, self).__init__(vadpy, options)

    def run(self):
        super(ModSourceHistogram, self).run()
        vad_combinations = product([0, 1], repeat = len(self.inputs))

        # initialize histograms:
        base_histogram = {}
        base_histograms = {}
        speech_histograms = {}
        noise_histograms = {}
        prob_histograms = {}
        lr_histograms = {}
        speech_frames_counts = {}
        noise_frames_counts = {}

        for comb_vec in vad_combinations:
            base_histogram[comb_vec] = COMB_MIN_VALUE

        source_names = set(elem.source_name for elem in self.vadpy.pipeline)
        for source_name in source_names:
            base_histograms[source_name] = deepcopy(base_histogram)
            speech_frames_counts[source_name] = 0
            noise_frames_counts[source_name] = 0

        speech_histograms = deepcopy(base_histograms)
        noise_histograms = deepcopy(base_histograms)
        prob_histograms = deepcopy(base_histograms)
        lr_histograms = deepcopy(base_histograms)

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

                prob_histograms[element.source_name][comb_vec] += 1
                if element.gt_labels[i][2]:
                    speech_histograms[element.source_name][comb_vec] += 1
                    speech_frames_counts[element.source_name] += 1
                else:
                    noise_histograms[element.source_name][comb_vec] += 1
                    noise_frames_counts[element.source_name] += 1

        # normalize histograms
        for source_name in prob_histograms:
            for comb in prob_histograms[source_name]:
                speech_histograms[source_name][comb_vec] /= speech_frames_counts[source_name]
                noise_histograms[source_name][comb_vec] /= noise_frames_counts[source_name]
                prob_histograms[source_name][comb_vec] /= (speech_frames_counts[source_name] +
                                                           noise_frames_counts[source_name])
                speech_val = speech_histograms[source_name][comb_vec]
                noise_val = noise_histograms[source_name][comb_vec]

            if noise_val == 0 or speech_val == 0:
                lr_histograms[source_name][comb] = 0.0
            elif noise_val == 0:
                lr_histograms[source_name][comb] = 1.0
            else:
                lr_histograms[source_name][comb] = speech_val / noise_val

        # update pipeline with histogram data
        self.add_result('speech', speech_histograms)
        self.add_result('noise', noise_histograms)
        self.add_result('lr', lr_histograms)
        self.add_result('p', prob_histograms)
