from vadpy.module import CompareModule
from vadpy.options import  Option

import logging 
log = logging.getLogger(__name__)

class ModAgreement(CompareModule):
    """Tests elements' labels for 'agreement'"""
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
                
            assert len(set( len(labels) for labels in lo_list)) == 1, \
                   'Labels objects section count differs'

            total_agreement_rate = 0.0
            majority_agreement_rate = 0.0

            frame_len = lo_list[0].frame_len
            sections_count = len(lo_list[0])

            for i in range(0, sections_count):
                combined_section = []
                for lo in lo_list:
                    combined_section.append(lo[i][2]) # i-th section, (start, end, --> voiced <-- ) tuple

                voiced_count = len([value for value in combined_section 
                                   if value])
                unvoiced_count = lo_count - voiced_count
                
                majority_agreement_rate += max(unvoiced_count, voiced_count) / lo_count
                if voiced_count == lo_count or unvoiced_count == lo_count:
                    total_agreement_rate += 1


            majority_agreement_rate /= sections_count
            total_agreement_rate /= sections_count

            if self.sep_sources:
                source_name = element.source_name

            try:
                source_rates[source_name].append( (majority_agreement_rate, total_agreement_rate) )
            except KeyError:
                source_rates[source_name] = [(majority_agreement_rate, total_agreement_rate), ]
            
        for source_name, rates in source_rates.items():
            majority_agreement_rate = sum(r[0] for r in rates) / len(rates)
            total_agreement_rate = sum(r[1] for r in rates) / len(rates)
            print(source_name)
            print('Majority agreement rate: {0:.3}%'.format(100 * majority_agreement_rate))
            print('Total agreement rate: {0:.3}%'.format(100 * total_agreement_rate))


