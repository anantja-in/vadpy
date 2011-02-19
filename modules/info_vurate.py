from vadpy.module import InfoModule
from vadpy.options import  Option

import logging 
log = logging.getLogger(__name__)

class ModVURate(InfoModule):
    """Compares the voiced/unvoiced rate of the elements

    Processes single input at a time
    """    
    labels_attr = Option('labels-attr', description = 'Labels attribute')

    def __init__(self, vadpy, options):
        super(ModVURate, self).__init__(vadpy, options)

    def run(self):
        super(ModVURate, self).run()

        for element in self.vadpy.pipeline:            
            labels = getattr(element, self.labels_attr)
            voiced_count = sum(1 for frame in labels
                               if frame[2])
            unvoiced_count = len(labels) - voiced_count
            
            element._info_vurate = voiced_count / float(unvoiced_count)
