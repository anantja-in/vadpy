from vadpy.module import CompareModule
from vadpy.options import  Option

import logging 
log = logging.getLogger(__name__)

class ModConfusion(CompareModule):
    """Tests elements' labels for TypeI and TypeII errors
    -----------------------------------------------------------------------
    |                           | H0 is True         | H1 is True         |
    |---------------------------|--------------------|--------------------|
    | Fail to reject H0         | Right decision     | Wrong, Type II err.|
    |                           | True positive      | False negative     |
    |---------------------------|--------------------|--------------------|
    | Reject H0                 | Wrong, Type I err. | Right decision,    |
    |                           | False positive     | True negative      |
    |---------------------------|--------------------|--------------------|
    """
    fscore_b = Option('fscore-b', float, "F-measurment's Beta parameter's value")

    def __init__(self, vadpy, options):
        super(ModConfusion, self).__init__(vadpy, options)

    def run(self):
        super(ModConfusion, self).run()
        assert len(set(self.inputs)) == 2, 'Confusion module requires two different inputs'

        # false positives/false negatives per source
        # the format of every tuple in dictionary is 
        # [True Positives, True Negatives, False Positives, False Negatives] tuple (list actually :)
        source_err = {} 
        source_name = 'All'

        for element in self.vadpy.pipeline:
            if self.sep_sources:
                source_name = element.source_name
            
            # Generate a list of decision (voiced/unvoiced) pairs for Labels objects
            # 
            labelsA = getattr(element, self.inputs[0])
            labelsB = getattr(element, self.inputs[1])
            
            if len(labelsA) != len(labelsB):
                log.warning('Labels length mismatch: {0} / {1}, auto-adjusting frame lengths.'.format(len(labelsA), len(labelsB)))
                min_flen = min(labelsA.frame_len, labelsB.frame_len)
                labelsA.frame_len = min_flen
                labelsB.frame_len = min_flen

            voicedAB = zip((voiced for start, stop, voiced in labelsA), # zip will concatenate up to min. length of the objects
                           (voiced for start, stop, voiced in labelsB))

            # Calculate False alarm and Miss rate
            tp = 0; tn = 0; fp = 0; fn = 0;
            for valA, valB in voicedAB:
                if valA:                # concluding, valA is a value 'Voiced' Ground Truth frame
                  if valB: tp += 1      # true positive
                  else:    fp += 1      # false positive, false alarm
                else:                     
                  if valB: fn += 1      # false negative, miss rate
                  else:    tn += 1      # true negative

            # Store error values to sources'  "errors summary"
            try:
                err = source_err[source_name]
                err[0] += tp
                err[1] += tn
                err[2] += fp
                err[3] += fn
            except KeyError:
                source_err[source_name] = [tp, tn, fp, fn]

        # convert results to percent domain
        for source_name, err in source_err.items():            
            tp = float(err[0])
            tn = float(err[1])
            fp = float(err[2])
            fn = float(err[3])
            tp_fp = tp + fp
            tn_fn = tn + fn

            tp /= tp_fp
            tn /= tn_fn
            fp /= tp_fp
            fn /= tn_fn

            B2 = self.fscore_b**2
            fscore = (1 + B2) * tp / \
                ((1 + B2) * tp + B2 * fn + fp)

            tp *= 100 # to percents
            tn *= 100 
            fp *= 100 
            fn *= 100
            # print the stuff to stdout
            print(source_name)
            print('{0:<25}{1:.3}%'.format('Miss Rate:',
                                            fp))
            print('{0:<25}{1:.3}%'.format('False Alarm Rate:',
                                            fn))
            print('{0:<25}{1:.3}'.format('F-Score:',
                                          fscore))
            # print('{0:<25}{1:.3}%'.format('True positives rate:',
            #                               tp))
            # print('{0:<25}{1:.3}%'.format('True negatives rate:',
            #                               fp))
            
            print('')
