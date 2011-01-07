import logging 

log = logging.getLogger(__name__)

from .pipeline import Pipeline
from .manager import ModuleManager
from .parser import parse

class VADpy(object):
    def __init__(self, settings, args):
        self.settings = settings
        self.pipeline = Pipeline(self)
        self._modules = []
        self._parse_arguments(args)

    def _parse_arguments(self, args):
        modules = parse(self.settings, args)
        manager = ModuleManager(self)

        for module, options in modules:
            assert module in manager, 'Cannot continue: Module "{0}" has not been loaded'.format(module)

            self._modules.append(
                manager.enable(module, options))

            
    def run(self):
        for module in self._modules:
            module.run()
