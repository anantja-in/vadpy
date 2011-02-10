import os
import logging 

log = logging.getLogger(__name__)

UNDEFINED = 0
LITTLE_ENDIAN = 0x2
BIG_ENDIAN = 0x4
FS_8000 = 0x8
BPS_16 = 0x10

class Element(object):
    def __init__(self, source_name, source_path, gt_path, flags = UNDEFINED):
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
        self._length = 0              # data length in seconds
        self.set_length()

    def set_length(self):
        try:
            if self.source_path:
                self._length = os.path.getsize(self.source_path) / (self.fs * (self.bps / 8.0))
        except OSError: # No such file or directory
            pass

    def __len__(self):
        if not self._length:
            self.set_length()
        if self._length:
            return self._length
        if self.gt_labels:
            return self.gt_labels.frame_len * len(self.gt_labels)
        if self.vad_labels:
            return self.gt_lanels.frame_len * len(self.gt_labels)        
        return 0

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
        return {'e_srcname' : self.source_name, 
                'e_srcdir' : source_dir, 
                'e_srcfile' : source_file, 
                'e_gtdir' : gt_dir, 
                'e_gtfile' : gt_file, 
                'e_voutdir' : vout_dir, 
                'e_voutfile' : vout_file, 
                }
