import collections

from .element import UNDEFINED

class Pipeline(object):
    def __init__(self, vadpy):
        self._elements = []

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

    def flush(self):
        self._elements = []

    def is_ready(self, raise_error = False):
        is_ready = all(elem.bps and elem.fs and elem.flags != UNDEFINED 
                       for elem in self._elements)
        if raise_error:
            assert is_ready, 'The pipeline is not ready to be processed'
        return is_ready
