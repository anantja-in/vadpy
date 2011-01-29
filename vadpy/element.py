import os
import logging 

log = logging.getLogger(__name__)

UNDEFINED = 0
LITTLE_ENDIAN = 0x2
BIG_ENDIAN = 0x4
FS_8000 = 0x8
BPS_16 = 0x10

_FS_FLAGS = [FS_8000, ]
_BPS_FLAGS = [BPS_16, ]
_ENDIAN_FLAGS = [LITTLE_ENDIAN, BIG_ENDIAN, ]


class Element(object):
    def __init__(self, source_name, source_path, gt_path, flags = UNDEFINED, set_length = True):
        """
        
        length - length in seconds
        """
        # defined by DB element
        self.flags = flags
        self.source_name = source_name
        self.source_path = source_path
        self.gt_path = gt_path
        self.gt_labels = None         # definet by IO module (reading GT)
        self.vout_path = ''           # defined by VAD module
        self.vad_labels = None        # defined by IO module (reading VAD output)
        self.length = 0               # file length in seconds
        if set_length:
            self.set_length()         # calculate and set length value

    def set_length(self):
        self.length = os.path.getsize(self.source_path) / (self.fs * (self.bps / 8.0)) 

    @property
    def bps(self):
        if self._flags & BPS_16:
            return 16
        raise Exception('Invalid BPS flag')

    @property
    def fs(self):
        if self._flags & FS_8000:
            return 8000
        raise Exception('Invalid FS flag')
    
    @property
    def flags(self):
        return self._flags

    @flags.setter
    def flags(self, value):
        self._flags = value

    @property
    def format_args(self):
        """Dynamic (built from element's arguments) string formatting arguments dictionary"""        
        source_dir, source_file = os.path.split(self.source_path)
        gt_dir, gt_file = os.path.split(self.source_path)
        vout_dir, vout_file = os.path.split(self.vout_path)
        return {'srcname' : self.source_name, 
                'srcdir' : source_dir, 
                'srcfile' : source_file, 
                'gtdir' : gt_dir, 
                'gtfile' : gt_file, 
                'voutdir' : vout_dir, 
                'voutfile' : vout_file, 
                }
