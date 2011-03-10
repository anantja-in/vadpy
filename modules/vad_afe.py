import logging 

from vadpy.module import SimpleVADModuleBase
from vadpy.element import BIG_ENDIAN, LITTLE_ENDIAN
from vadpy.options import Option

log = logging.getLogger(__name__)


class VADAFE(SimpleVADModuleBase):
    """Advanced Front-Ent codec (AFE) VAD module"""
    def __init__(self, vadpy, options):
        super(VADAFE, self).__init__(vadpy, options)
#        raise Exception('Not implemented')

    def _get_exec_options(self, element):
        if element.flags & BIG_ENDIAN:
            opt_before_args = ['-swap']

        return opt_before_args, []
