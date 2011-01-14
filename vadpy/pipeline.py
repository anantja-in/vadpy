UNDEFINED = 0
LITTLE_ENDIAN = 0x2
BIG_ENDIAN = 0x4
FS_8000 = 0x8
BPS_16 = 0x10

class Pipeline(object):
    def __init__(self, vadpy):
        self._elements = []
        self._flags = None

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

    @property
    def flags(self):
        return self._flags

    def flags(self, value):
        if self._flags != UNDEFINED:
            assert self._flags == value, "The pipeline must be flushed before setting different flags"
        self._flags = value

    def flush(self):
        self._elements = []
        self._flags = UNDEFINED
