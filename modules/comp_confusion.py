from vadpy.module import CompareModule
from vadpy.options import  Option
from vadpy.labels import equalize_framelen

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

    |-----------|-----|
    | GT  | VAD | Err | Total error rate = Fn + Fp / (Tp + Fn + Tn + Fp)
    |-----|-----|-----|
    |  1  |  1  | Tp  |
    |  1  |  0  | Fn  | Fn rate = Fn / (Tp + Fn)
    |  0  |  0  | Tn  |
    |  0  |  1  | Fp  | Fp rate = Fp / (Tn + Fp)
    |-----------------|
    """
    # fscore_b = Option('fscore-b', float, "F-measurment's Beta parameter's value")
    cmp_size=Option('cmp-size', int, 'Amount of 2nd labels object frames to be treated as a single frame')

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
            gt_labels = getattr(element, self.inputs[0])
            vad_labels = getattr(element, self.inputs[1])
            
            if len(gt_labels) != len(vad_labels):
                log.warning('Labels length mismatch: {0} / {1}, equlizing frame lengths.'.format(
                        len(gt_labels), len(vad_labels)))

                equalize_framelen(gt_labels, vad_labels)

            # zip will concatenate up to min. length of the objects
            voicedAB = zip((voiced for start, stop, voiced in gt_labels), 
                           (voiced for start, stop, voiced in vad_labels))

            # Calculate False alarm and Miss rate
            tp = 0; tn = 0; fp = 0; fn = 0;

            half_cmp_size = int(self.cmp_size / 2)


            for i in range(0, len(voicedAB)):
                valA = voicedAB[i][0]
                
                if (half_cmp_size > 0 and 
                    half_cmp_size < i < len(voicedAB) - half_cmp_size):
                    valB = bool(round(sum(vAB[1] for vAB in voicedAB[i - half_cmp_size : i + half_cmp_size]) 
                                 / float(self.cmp_size)))
                else:
                    valB = voicedAB[i][1]

                if valA:                # concluding, valA is a value 'Voiced' Ground Truth frame
                  if valB: tp += 1      # true positive
                  else:    fn += 1      # false negative, miss 
                else:                     
                  if valB: fp += 1      # false positive, false alarm
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
                        
            # B2 = self.fscore_b**2
            # fscore = (1 + B2) * tp / \
            #     ((1 + B2) * tp + B2 * fn + fp)
            length = tp + tn + fp + fn;
            gt_voiced = fn + tp
            gt_unvoiced = fp + tn

            mr  = 100 * fn / (tp + fn)
            far = 100 * fp / (tn + fp)
            vur = gt_voiced / gt_unvoiced
            #total_len = tn + fn + tp + fp
            
            print(source_name)
            print('{0:<25}{1:.3}'.format('Miss rate:', mr))
            print('{0:<25}{1:.3}'.format('False alarm rate:', far))
            print('{0:<25}{1:.3}'.format('Speech/Nonspeech rate:', vur))
            print('')



