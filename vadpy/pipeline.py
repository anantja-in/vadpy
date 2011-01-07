class Pipeline(object):
    def __init__(self, vadpy):
        self._entities = []

    def add(self, entities):
        self._entities.extend(entities)

    def __getitem__(self, item):
        return self._entities[item]

    def __iter__(self):
        return self._entities.__iter__()

    def __contains__(self, entity):
        return entity in self._entities

    def slice(self, count):
        """Generator, returns items from pipe by 'count' slices"""
        i = 0
        while True:
            sliced_entities = self._entities[i:i+count]

            if sliced_entities:
                yield sliced_entities
                i += count
            else:
                return 
        
