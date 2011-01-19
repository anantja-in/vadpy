import collections

UNDEFINED = 0
LITTLE_ENDIAN = 0x2
BIG_ENDIAN = 0x4
FS_8000 = 0x8
BPS_16 = 0x10

_FS_FLAGS = [FS_8000, ]
_BPS_FLAGS = [BPS_16, ]
_ENDIAN_FLAGS = [LITTLE_ENDIAN, BIG_ENDIAN, ]

class Pipeline(object):
    def __init__(self, vadpy):
        self._elements = []
        self._flags = UNDEFINED

    def add(self, *elements):
        self._elements.extend(elements)

    def __getitem__(self, item):
        return self._elements[item]

    def __iter__(self):
        if self.is_ready(raise_error = True):
            return self._elements.__iter__()

    def __contains__(self, entity):
        return entity in self._elements

    def slice(self, count):
        """Generator, returns items from pipe by 'count' slices"""
        i = 0
        while True:
            sliced_elements = self._elements[i:i+count]

            if sliced_elements:
                yield sliced_elements
                i += count
            else:
                return 

    def flush(self, flush_flags = True):
        self._elements = []
        if flush_flags:
            self._flags = UNDEFINED

    def is_ready(self, raise_error = False):
        is_ready = all([self.flags != UNDEFINED, self.bps, self.fs])
        if raise_error:
            assert is_ready, 'The pipeline is not ready to be processed'
        return is_ready

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
        if self._flags != UNDEFINED and value != UNDEFINED:
            assert self._flags == value, 'The pipeline must be flushed before setting different flags '
        self._flags = value
