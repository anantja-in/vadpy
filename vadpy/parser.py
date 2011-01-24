import sys
import logging
import re
from copy import deepcopy 

from .error import ParseError

log = logging.getLogger(__name__)


class SeqOptions(object):
    def __init__(self, settings):

        self._settings = settings
        self._macros = settings.MACROS
        
        self.help_required = False

    def parse(self):
        help_modules = self._parse_help()

        if self.help_required:
            return help_modules
        else:
            return self._parse_args()
        
    def _parse_help(self):
        argv = sys.argv
        if len(argv) == 1 or len(argv) >= 2 and argv[1] in ('-h' or '--help'):
            self.help_required = True
            if len(argv) == 3:
                return argv[2]
        return None
        
    def _parse_args(self):
        # vad.py [OPTIONS] ! module property1=val property2=val ... \
        #                    property_flag1 property_flag2 ... ! module2 ... !
        # Cases:
        # ! corpus ! intput ! VAD program ! error_metrics ! output
        # 
        args = ' '.join(sys.argv) + ' '
        args = self._macro_replace(args)

        argv = args.split('!')[1:]
        modules = []

        if len(argv) == 1:        
            return []

        for sarg in argv:
            module = None
            quote = False
            module_args = {}
            buf = ''
            for char in sarg: #iostamps re=(?P<hh>\d+):(?P<mm>\d+):(?P<ss>\d+) split=" " 
                if char != ' ':
                    if char == '"':
                        quote = not quote
                    else:
                        buf += char

                if char == ' ':
                    if quote:
                        buf += char
                    elif len(buf):
                        if not module: # create a module
                            module = buf
                            buf = ''
                        else:
                            if not quote: # not module and NOT quote (e.g. quotation is finished)
                                if '=' in buf:
                                    name, val = buf.split('=')
                                    module_args[name] = val
                                    buf = ''
            if module:
                modules.append( (module, deepcopy(module_args)) )
        return modules

    def _macro_replace(self, s):
        s_old = s
        for macro in self._macros:
            s = s.replace(' ' + macro + ' ', 
                          ' ' + self._format(self._macros[macro]) + ' ')
        if s != s_old:
            s = self._macro_replace(s)
        return s

    def _format(self, macro):
        return macro.format(root = self._settings.ROOT,
                            bindir = self._settings.BINDIR,
                            outdir = self._settings.OUTDIR,
                            dbdir = self._settings.DBDIR,
                            framelen = self._settings.FRAMELEN,)
