import logging 

from vadpy.module import SimpleVADModuleBase
from vadpy.element import BIG_ENDIAN

log = logging.getLogger(__name__)


class VADG729(SimpleVADModuleBase):
    """G729 Annex B VAD algorithm module"""
    def _get_exec_options(self, element):
        return [], element.flags & BIG_ENDIAN and ['-b'] or []
