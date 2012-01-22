import os
import logging

from vadpy.module import Module
from vadpy.options import Option

log = logging.getLogger(__name__)


class ModPipeline(Module):
    """Pipeline control module"""
    ACTION_FLUSH = 'flush'
    action = Option(description = 'Pipeline action: flush| ')

    def __init__(self, vadpy, options):
        super(ModPipeline, self).__init__(vadpy, options)

    def __run__(self):
        super(ModPipeline, self).run()

        if self.action == self.ACTION_CLEAR:
            self.vadpy.pipeline.flush()
