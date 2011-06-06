from vadpy.module import ComputeModule
from vadpy.options import  Option
from vadpy.labels import equalize_framelen

import math

import logging 
log = logging.getLogger(__name__)

class ModCorrelation(ComputeModule):
    """Compute correlation between inputs
    -----------------------------------------------------------------------
    |                           | VAD_1 is correct   | VAD_1 is wrong     |
    |---------------------------|--------------------|--------------------|
    | VAD_1 is correct          |         a          |         b          |
    |                           |                    |                    |
    |---------------------------|--------------------|--------------------|
    | VAD_1 is wrong            |         c          |         d          |
    |                           |                    |                    |
    |---------------------------|--------------------|--------------------|
    Q = (a*d - b*c) / (a*d + b*c)
    p = a*b - b*c / sqrt((a + b) * (c + d) * (a + c) * (b + d))
    """

    def __init__(self, vadpy, options):
        super(ModCorrelation, self).__init__(vadpy, options)

    def run(self):
        super(ModCorrelation, self).run()
        assert len(set(self.inputs)) == 3, 'Q-statistics module requires three different inputs (GT, VAD1, VAD2)'

        # false positives/false negatives per source
        # the format of every tuple in dictionary is 
        # [True Positives, True Negatives, False Positives, False Negatives] tuple (list actually :)

        a_total = 0.0
        b_total = 0.0
        c_total = 0.0
        d_total = 0.0

        for element in self.vadpy.pipeline:            
            gt_labels = getattr(element, self.inputs[0])
            vad1_labels = getattr(element, self.inputs[1])
            vad2_labels = getattr(element, self.inputs[2])
            
            if len(set([len(gt_labels), len(vad1_labels), len(vad2_labels)])) != 1:
                log.warning('Labels length mismatch: {0} / {1} / {2}, equlizing frame lengths.'.format(
                        len(gt_labels), len(vad1_labels), len(vad2_labels) ))
                equalize_framelen(gt_labels, vad1_labels, vad2_labels)

            speechData = zip((int(speech) for start, stop, speech in gt_labels), 
                             (int(speech) for start, stop, speech in vad1_labels),
                             (int(speech) for start, stop, speech in vad2_labels))

            a = 0; b = 0; c = 0; d = 0;

            for i in range(0, len(speechData)):
                valGT = speechData[i][0]
                valV1 = speechData[i][1]
                valV2 = speechData[i][2]
                
                if valV1 == valGT and valV2 == valGT:
                    a += 1
                elif valV1 != valGT and valV2 == valGT:
                    b += 1
                elif valV1 == valGT and valV2 != valGT:
                    c += 1
                else:
                    d += 1

            a_total += a
            b_total += b
            c_total += c
            d_total += d

        length = a_total + b_total + c_total + d_total;
        a = a_total / length
        b = b_total / length
        c = c_total / length
        d = d_total / length

        corrQ = (a*d - b*c) / (a*d + b*c)
        corrp = (a*d - b*c) / math.sqrt((a + b)*(c + d)*(a + c)*(b + d))

        self.add_result('corrQ', corrQ)
        self.add_result('corrp', corrp)


    def _format_results(self):
        res = self._get_results()
        corrQ = res.corrQ
        corrp = res.corrp
        return ('{0:<25}{1:.3}\n'.format('Q-Statistics (Q):', corrQ) + 
                '{0:<25}{1:.3}'.format('Correlation (p):', corrp)
                )
