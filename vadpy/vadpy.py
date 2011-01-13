import logging 

log = logging.getLogger(__name__)

from .pipeline import Pipeline
from .manager import ModuleManager
from .parser import SeqOptions

class VADpy(object):
    def __init__(self, settings):
        self.settings = settings
        self.pipeline = Pipeline(self)
        self.options = SeqOptions(settings)

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
            if modules: # modules is a simple string variable here
                if modules in self.settings.MACROS:
                    print('VADpy macro: {0} '.format(self.settings.MACROS[modules]))
                else:
                    module = manager[modules]
                    print('\n{0}'.format(module))
            else:
                # print general program help
                print 'VADpy help'
            
            exit()
                
        for module, options in modules:
            self._modules.append(
                manager.enable(module, options))
        
            
    def run(self):
        for module in self._modules:
            module.run()
