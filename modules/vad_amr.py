import logging 

from vadpy.module import SimpleVADModuleBase
from vadpy.element import BIG_ENDIAN, LITTLE_ENDIAN
from vadpy.options import Option

log = logging.getLogger(__name__)


class VADAMR(SimpleVADModuleBase):
    """Adaptive Multi-Rate audio codec (AMR) VADpy module"""

    def _get_exec_options(self, element):
        opt_before_args = ['MR122', ] # see allmodes.txt in AMR source directory
        opt_after_args = []
        if element.flags & BIG_ENDIAN:
            opt_after_args = ['b', ]
        elif element.flags & LITTLE_ENDIAN:
            opt_after_args = ['l', ]

        return opt_before_args, opt_after_args


