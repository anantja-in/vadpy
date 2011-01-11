import logging 

log = logging.getLogger(__name__)

UNDEFINED = 0
LITTLE_ENDIAN = 2
BIG_ENDIAN = 4

class Element(object):
    def __init__(self, source_name, length, source_path, gt_path, flags = UNDEFINED):
        # defined by DB element
        self.source_name = source_name
        self.source_path = source_path
        self.gt_path = gt_path              
        self.flags = flags
        self.length = length               # file length in seconds

        # defined by VAD module
        # self.vad_output_path = None

        # definet by IO module (reading GT)
        # self.gt_data = None
