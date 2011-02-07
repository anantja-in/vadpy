import logging 

from vadpy.module import MatlabVADModuleBase
from vadpy.element import LITTLE_ENDIAN, BIG_ENDIAN
from vadpy.options import Option

log = logging.getLogger(__name__)


class VADMatlab(MatlabVADModuleBase):
    """Matlab-based VADs helper module

    Path formatting:
    {script} - uses "script" option's value in path, e.g. ... voutdir="{outroot}/matlab/{{script}}"
    """
    script = Option(description = 'VAD function name')
    fread = Option(description = 'Length of a signal in each fread iteration (in seconds)')
    args = Option(description = 'Additional arguments to be passed to matlab script')

    def __init__(self, vadpy, options):
        super(VADMatlab, self).__init__(vadpy, options)
        assert self.filecount > 0, 'Filecount must be > 0'

        self._execargs['script'] = self.script
        self._execargs['fread_len'] = self.fread
        self._execargs['vad_args'] = self.args

        self._execlist = ['{engine}', 
                          "'{script}'",
                          "'{vad_args}'",
                          "'{endianness}'", 
                          "{fread_len}",
                          "'{in_paths}'",
                          "'{gt_paths}'",
                          "'{out_paths}'",
                          ]

    def _get_vout_path(self, element):
        self.voutdir = self.voutdir.format(engine = self.engine,
                                           script = self.script)
        return super(VADMatlab, self)._get_vout_path(element)
                                            
    
    def run(self):                                  
        super(VADMatlab, self).run()
        

