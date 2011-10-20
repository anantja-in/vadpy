from vadpy.module import ComputeModule
from vadpy.options import  Option
from vadpy.labels import equalize_framelen

from itertools import product
import math

import logging
log = logging.getLogger(__name__)

COMB_MIN_VALUE = 1.0

class ModConditionHistogram(ComputeModule):
    """Condition-based histogram calculator"""
    def __init__(self, vadpy, options):
        super(ModFusionHistogram, self).__init__(vadpy, options)

    def run(self):
        super(ModFusionHistogram, self).run()
