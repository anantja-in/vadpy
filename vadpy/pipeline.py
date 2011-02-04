import collections
import logging 

from .element import UNDEFINED

log = logging.getLogger(__name__)


class Pipeline(object):
    def __init__(self, vadpy):
        self._elements = []

    def add(self, *elements):
        self._elements.extend(elements)
        log.debug('{0} elements have been added to the pipeline'.format(len(elements)))

    def __getitem__(self, item):
        return self._elements[item]

    def __iter__(self):
        assert self.ready, 'The pipeline is not ready to be processed'
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

    @property
    def ready(self):
        is_ready = all(elem.bps and elem.fs and elem.flags != UNDEFINED 
                       for elem in self._elements)
        return is_ready
    
    @property
    def monotonic(self):
        return len(set(elem.flags for elem in self._elements)) <= 1
