from vadpy.module import CompareModule
from vadpy.options import  Option

import logging 
log = logging.getLogger(__name__)

class ModAgreement(CompareModule):
    """Tests elements' labels for 'agreement'

    This module is made for testing the percentage of 'agreement' rates between N labels' objects
    E.g. O1, O2, O3 are input objects with equal frames count

    O1 O2 O3    M   T   MR    TR
    0  1  0     2   0   2/3   0
    1  0  0     2   0   2/3   0
    1  1  0     2   0   2/3   0
    1  1  1     3   3    1    1
    1  1  1     3   3    1    1
    0  0  0     3   3    1    1
    0  0  1     2   0   2/3   0

    Here, 'M' determines 'majority agreement', 'T' - total agreement. 
    Thus, 'MR' is majority agreement rate, 'TR' - total agreement rate. 
    By summing the rates, and diving them to the total amount of frames, 
    we can see that majority agreement rate is ~ 80%
    and total agreement rate is ~ 42%
    """    
    def __init__(self, vadpy, options):
        super(ModAgreement, self).__init__(vadpy, options)

    def run(self):
        super(ModAgreement, self).run()
        source_name = 'All'
        source_rates = {}

        for element in self.vadpy.pipeline:            
            lo_list = []                        # labels object aka "lo"
            for attr in self.inputs:
                lo_list.append(getattr(element, attr))
            lo_count = float(len(lo_list))
                
            frames_count = [len(labels) for labels in lo_list]
            assert len(set(frames_count)) == 1, \
                   'Labels objects frame count differs: {0}'.format(frames_count)

            agreement_rate = 0.0
            majority_voiced_rate = 0.0

            frame_len = lo_list[0].frame_len
            frames_count = len(lo_list[0])

            for i in range(0, frames_count):
                combined_frame = []
                for lo in lo_list:
                    combined_frame.append(lo[i][2]) # i-th frame, (start, end, --> voiced <-- ) tuple

                voiced_count = sum(1 for value in combined_frame 
                                   if value)
                unvoiced_count = lo_count - voiced_count
                
                majority_voiced_rate += voiced_count / lo_count
                if voiced_count == lo_count or unvoiced_count == lo_count:
                    agreement_rate += 1


            majority_voiced_rate /= frames_count
            agreement_rate /= frames_count

            if self.sep_sources:
                source_name = element.source_name

            try:
                source_rates[source_name].append( (majority_voiced_rate, agreement_rate) )
            except KeyError:
                source_rates[source_name] = [(majority_voiced_rate, agreement_rate), ]
            
        for source_name, rates in source_rates.items():
            majority_voiced_rate = sum(r[0] for r in rates) / len(rates)
            agreement_rate = sum(r[1] for r in rates) / len(rates)
            print(source_name)
            print('Majority voiced rate: {0:.3}%'.format(100 * majority_voiced_rate))
            print('Total agreement rate: {0:.3}%'.format(100 * agreement_rate))


