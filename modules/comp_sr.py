from vadpy.module import ComputeModule
from vadpy.options import  Option
from vadpy.labels import equalize_framelen

import math

import logging
log = logging.getLogger(__name__)

class ModSR(ComputeModule):
    """Compute speech to non-speech rate"""

    def __init__(self, vadpy, options):
        super(ModSR, self).__init__(vadpy, options)

    def run(self):
        super(ModSR, self).run()

        sr = {}
        for input_name in self.inputs:
            for element in self.vadpy.pipeline:
                labels = getattr(element, input_name)

                sp_labels = 0.0
                non_sp_labels = 0.0
                for start, stop, speech_flag in  labels:
                    if speech_flag:
                        sp_labels += 1
                    else:
                        non_sp_labels += 1
            sr[input_name] =  sp_labels / non_sp_labels

        self.add_result('sr', sr)

    def _format_results(self):
        sr = self._get_results().sr
        ret_str = ''
        for input_name in sr:
            sr_val = sr[input_name]
            ret_str += '{0} / {1:<25}{2:.3}; ({3:.3}% speech)\n'.format(
                'Speech/Non-speech rate',
                input_name,
                sr_val,
                100 * sr_val / (1 + sr_val))
        return ret_str
