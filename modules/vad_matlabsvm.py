import logging 

from vadpy.module import MatlabVADModuleBase
from vadpy.element import LITTLE_ENDIAN, BIG_ENDIAN
from vadpy.options import Option

log = logging.getLogger(__name__)


class VADMatlabSVM(MatlabVADModuleBase):
    """Matlab-based VADs helper module

    Path formatting:
    {script} - uses "script" option's value in path, e.g. ... voutdir="{outroot}/matlab/{{script}}"
    """
    script = Option(description = 'VAD function name')
    frame_len = Option('frame-len', description = 'Labels frame length')

    def __init__(self, vadpy, options):
        super(VADMatlabSVM, self).__init__(vadpy, options)

        self._execargs['script'] = self.script
        self._execargs['frame_len'] = self.frame_len

        self._execlist = ['{engine}', 
                          "'{script}'",
                          "'{endianness}'", 
                          "'{frame_len}'",
                          "'{in_paths}'",
                          "'{gt_paths}'",
                          "'{out_paths}'",
                          ]

    def _get_vout_path(self, element):
        self.voutdir = self.voutdir.format(engine = self.engine,
                                           script = self.script)
        return super(VADMatlabSVM, self)._get_vout_path(element)
                                            
    
    def run(self):                                  
        super(VADMatlabSVM, self).run()
        

