import logging 

from vadpy.module import SimpleVADModuleBase
from vadpy.element import BIG_ENDIAN, LITTLE_ENDIAN
from vadpy.options import Option

log = logging.getLogger(__name__)


class VADAMR(SimpleVADModuleBase):
    """Adaptive Multi-Rate audio codec (AMR) VADpy module"""
    mode = Option(default = '1', 
                  description = 'AMR VAD to be used (values 1 or 2)' )

    def __init__(self, vadpy, options):
        super(VADAMR, self).__init__(vadpy, options)

    def run(self):
        self._exec_path += self.mode
        super(VADAMR, self).run()

    def _get_exec_options(self, element):
        opt_before_args = ['MR122', ] # see allmodes.txt in AMR source directory
        opt_after_args = []
        if element.flags & BIG_ENDIAN:
            opt_after_args = ['b', ]
        elif elements.flags & LITTLE_ENDIAN:
            opt_after_args = ['l', ]

        assert not opt_after_args, 'Non-compatible endianness'
        return opt_before_args, opt_after_args

    def __init__(self, vadpy, options):
        super(VADAMR, self).__init__(vadpy, options)

    def run(self):
        super(VADAMR, self).run()

    def _get_exec_options(self, element):
        return [], element.flags & BIG_ENDIAN and ['-b'] or []
