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

    def __init__(self, vadpy, options):
        super(ModConfusion, self).__init__(vadpy, options)

    def run(self):
        super(ModConfusion, self).run()
        assert len(set(self.inputs)) == 2, 'Confusion module requires two different inputs'

        # false positives/false negatives per source
        # the format of every tuple in dictionary is 
        # [True Positives, True Negatives, False Positives, False Negatives] tuple (list actually :)
        source_err = {} 
        for element in self.vadpy.pipeline:
            if self.sep_sources:
                source_name = element.source_name
            else:
                source_name = 'All'
            
            # Generate a list of decision (voiced/unvoiced) pairs for Labels objects
            # 
            labelsA = getattr(element, self.inputs[0])
            labelsB = getattr(element, self.inputs[1])            
            if len(labelsA) != len(labelsB):
                log.warning('Labels length mismatch: {0} / {1}'.format(len(labelsA), len(labelsB)))

            voicedAB = zip((voiced for start, stop, voiced in labelsA), # zip will concatenate up to min. length of the objects
                           (voiced for start, stop, voiced in labelsB))

            # Calculate False alarm and Miss rate
            tp = 0; tn = 0; fp = 0; fn = 0;
            for valA, valB in voicedAB:
                if valA:                # concluding, valA is Ground truth value 'Voiced'
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
            tp = err[0]
            tn = err[1]
            fp = float(err[2])
            fn = float(err[3])
            tp_fp = tp + fp
            tn_fn = tn + fn

            tp /= tp_fp
            tn /= tn_fn
            fp /= tp_fp
            fn /= tn_fn

            fp *= 100 # to percents
            fn *= 100
            # print the stuff to stdout
            print(source_name)
            print('FRR: {0:.10}%'.format(fp))
            print('FAR: {0:.10}%'.format(fn))
            print('')

    
