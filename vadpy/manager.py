import os
import imp
import logging

from .error import ModuleNotFoundError, ParseError
from . import module

log = logging.getLogger(__name__)

class ModuleManager(object):
    """Modules manager class able to locate and load modules"""
    def __init__(self, vadpy):
        self.vadpy = vadpy
        self._modules_dirs = vadpy.settings.PATH
        self._modules = {}          # enabled modules {name : module}
        self._sorted_mod_names = [] # modules' names sorted by base class
        self._base_modules = [module.Module,
                              module.IOModule,
                              module.DBModule,
                              module.VADModule,
                              module.SimpleVADModuleBase,
                              module.MatlabVADModuleBase]
        self._scan()             # find and store modules

    def enable(self, name, options):
        """Create and return an instance of an Module-derived class"""
        name = name.lower()
        if name not in self:
            raise ModuleNotFoundError(name)

        module_class = self[name]
        module_object = module_class(self.vadpy, options)
        log.debug('Module {0} has been enabled'.format(name))
        return module_object

    def _scan(self):
        """Search for modules in vadpy modules directories"""
        # modules' base classes that should not(!) be loaded by manager
        # base_classes = [cls for cls in module.__dict__.values()
        #                 if isinstance(cls, type) and
        #                 issubclass (cls, module.Module)]
        # and attr not in base_classes]
        for edir in self._modules_dirs:
            if not os.path.exists(edir):
                log.debug("{0} doesn't exist".format(edir))
                continue

            dir_files = [fname for fname in os.listdir(edir)
                         if fname.endswith('py')]
            for fname in dir_files:
                path = os.path.join(edir, fname)
                try:
                    pymod = imp.load_source(fname[:-3], path) # somename.py -> somename
                except Exception as e:
                    log.error('Error loading module(s) from {0}: {1}'.format(path, str(e)))
                    if log.getEffectiveLevel() == logging.DEBUG:
                        raise e
                    else:
                        continue

                module_classes = [attr for attr in pymod.__dict__.values()
                                  if isinstance(attr, type) and
                                  issubclass (attr, module.Module) and
                                  attr not in self._base_modules]
                if len(module_classes) == 0:
                    log.debug('No Module sub-classes found in {0}'.format(path))

                for cls in module_classes:
                    self._modules[cls.__name__.lower()] = cls

    def __len__(self):
        return len(self._modules)

    def __getitem__(self, key):
        return self._modules[key]

    def __iter__(self):
        return (name for name, cls in sorted(self._modules.items(), key=lambda p: p[1].__bases__)).__iter__()

    def __contains__(self, item):
        return item in self._modules
