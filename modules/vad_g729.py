import logging 

from vadpy.module import SimpleVADModuleBase
from vadpy.element import BIG_ENDIAN

log = logging.getLogger(__name__)


class VADG729(SimpleVADModuleBase):
    def __init__(self, vadpy, options):
        super(VADG729, self).__init__(vadpy, options)

    def run(self):
        super(VADG729, self).run()

    def _get_exec_options(self, element):
        return [], element.flags & BIG_ENDIAN and ['-b'] or []
