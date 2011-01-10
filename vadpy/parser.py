import logging
import re
from copy import deepcopy 

from .error import ParseError

log = logging.getLogger(__name__)

def parse(settings, args):
    # vad.py [OPTIONS] ! module property1=val property2=val ... \
    #                    property_flag1 property_flag2 ... ! module2 ... !
    # Cases:
    # ! corpus ! intput ! VAD program ! error_metrics ! output
    # 
    args += ' '
    args = macro_replace(args, settings)

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


def macro_replace(s, settings):
    s_old = s
    for macro in settings.MACROS:
        s = s.replace(' ' + macro + ' ', 
                      ' ' + settings.format(settings.MACROS[macro]) + ' ')
    if s != s_old:
        s = macro_replace(s, settings)
    return s
    
