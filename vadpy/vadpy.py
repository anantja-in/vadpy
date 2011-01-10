import logging 

log = logging.getLogger(__name__)

from .pipeline import Pipeline
from .manager import ModuleManager
from .parser import SeqOptions

class VADpy(object):
    def __init__(self, settings):
        self.settings = settings
        self.pipeline = Pipeline(self)
        self.options = SeqOptions(settings.MACROS, settings.format)

        self._modules = []
        self._parse_arguments()

    def _parse_arguments(self):        
        # 
        # this parsing should be rewritten into a normal module
        # I believe, it's worth of a Python project :)
        # 
        modules = self.options.parse()
        manager = ModuleManager(self)

        if self.options.help_required:
            # print module help
            if modules:
                module = manager[modules[0]]
                print(module.__doc__)
            else:
                # print general program help help
                pass
            exit()
                
        for module, options in modules:
            self._modules.append(
                manager.enable(module, options))
        
            
    def run(self):
        for module in self._modules:
            module.run()
