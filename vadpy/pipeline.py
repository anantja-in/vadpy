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

    def add(self, elements):
        self._elements.extend(elements)

    def __getitem__(self, item):
        return self._elements[item]

    def __iter__(self):
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

    def flush(self):
        self._elements = []
        self._flags = UNDEFINED

    def is_ready():
        return all(self.flags != UNDEFINED, self.bps, self.fs)

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
