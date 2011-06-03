import sys
import logging 

log = logging.getLogger(__name__)

from .pipeline import Pipeline
from .manager import ModuleManager
from .parser import SeqOptions
from .module import DBModule

class VADpy(object):
    def __init__(self, settings):
        self.settings = settings
        self.pipeline = Pipeline(self)
        self.options = SeqOptions(self)        
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
            if modules: # "modules" is a simple string variable here
                if modules in self.settings.MACROS:
                    print('VADpy macro: {0} '.format(self.settings.MACROS[modules]))
                else:                    
                    module = manager[modules]
            else:
                exec_name = sys.argv[0]
                # print general program help
                print('VADpy - the ultimate VAD framework')
                print('Usage:\n{0} [OPTIONS] [MODULES SEQUENCE]\n'.format(exec_name))
                print('Modules:\n{0:<20}Description'.format('Name'))
                                                             
                for module in manager:
                    mod = manager[module]
                    print('{0:<20}{1}'.format(mod.__name__, str(mod.__doc__).split('\n')[0]))
            exit()
                
        for module, options in modules:
            self._modules.append(
                manager.enable(module, options))
                    
    def run(self):
        for module in self._modules:
            if not len(self.pipeline) and not issubclass(module.__class__, DBModule):
                return
            module.pre_run()
            module.run()
            module.post_run()
