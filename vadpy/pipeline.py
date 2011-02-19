import logging 
import collections

from .element import UNDEFINED

log = logging.getLogger(__name__)

class Pipeline(object):
    def __init__(self, vadpy):
        self._elements = []
        self._counter = 0

    def add(self, *elements):
        for element in elements:
            element.id = self._counter
            self._counter += 1

        self._elements.extend(elements)
        log.debug('{0} elements have been added to the pipeline'.format(len(elements)))

    def __getitem__(self, item):
        return self._elements[item]

    def __iter__(self):
        assert self.is_ready(), 'The pipeline is not ready to be processed'
        return self._elements.__iter__()

    def __contains__(self, entity):
        return entity in self._elements

    def __len__(self):
        return len(self._elements)

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
        self._counter = 0

    def is_ready(self):
        is_ready = all(elem.bps and elem.fs and elem.flags != UNDEFINED 
                       for elem in self._elements)
        return is_ready
    
    def is_monotonic(self):
        return len(set(elem.flags for elem in self._elements)) <= 1
