from vadpy.module import CompareModule
from vadpy.options import  Option

import logging 
log = logging.getLogger(__name__)

class ModConfusion(CompareModule):
    """Tests elements' labels for TypeI and TypeII errors"""
    
    def __init__(self, vadpy, options):
        super(ModCompare, self).__init__(vadpy, options)
        
    def run(self):
        super(ModConfusion, self).run()
        assert self.
        # false positives/false negatives per source
        fp = {}
        fn = {}
        for element in self.vadpy.pipeline:
            

    
