#!/usr/bin/env python
import sys
import logging 
import logging.handlers
import traceback

import settings
from vadpy import VADpy
log = logging.getLogger(__name__)


def main():
    try:
        setup_logging()
        vadpy = VADpy(settings)
        vadpy.run()
    except Exception as e:
        log.critical(str(e))
        exc_type, exc_value, exc_traceback = sys.exc_info()
        traceback.print_tb(exc_traceback, limit = None, file = sys.stdout)
        print('Error: {0}'.format(e))
        exit(1)


def setup_logging():
    console_format = '%(levelname)-8s %(message)s'
    loglevel = logging.DEBUG

    if  '-dt' in sys.argv:
        loglevel = logging.DEBUG
        console_format += ' (%(name)s)' # add module name in debug mode
    elif '-d' in sys.argv:
        loglevel = logging.DEBUG
        # add module name and message time in debug mode
        console_format = "%(asctime)-10s" + console_format + ' (%(name)s)' 
    elif  '-q' in sys.argv or '--quiet' in sys.argv:
        loglevel = logging.CRITICAL
    else: #'-i' in sys.argv or '--info' in sys.argv:
        loglevel = logging.INFO    

    # Logging to terminal
    logging.basicConfig(level = loglevel, 
                        format = console_format,
                        datefmt='%H:%M:%S',)


if __name__ == '__main__':
    main()
