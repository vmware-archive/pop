'''
This module is used to set up logging for pop projects and injects logging
options into conf making it easy to add robust logging
'''
# Import python libs
import logging


LEVELS = {'debug': logging.DEBUG,
          'info': logging.INFO,
          'warning': logging.WARNING,
          'error': logging.ERROR,
          'critical': logging.CRITICAL}


def conf(hub, name):
    '''
    Return the conf dict for logging, this should be merged OVER by the loaded
    config dict(s)
    '''
    #TODO: Make this more robust to handle more logging interfaces
    ldict = {
        'log_file':
            {
            'default': f'{name}.log',
            'help': 'The location of the log file',
            },
        'log_level':
            {
            'default': 'info',
            'help': 'Set the log level, either quiet, info, warning, or error',
            },
        'log_fmt_logfile':
            {
            'default': '%(asctime)s,%(msecs)03d [%(name)-17s][%(levelname)-8s] %(message)s',
            'help': 'The format to be given to log file messages',
            },
        'log_fmt_console':
            {
            'default': '[%(levelname)-8s] %(message)s',
            'help': 'The log formatting used in the console',
            },
        'log_datefmt':
            {
            'default': '%H:%M:%S',
            'help': 'The date format to display in the logs',
            },
        }
    return ldict


def setup(hub, conf):
    '''
    Given the configuration data set up the logger
    '''
    level = LEVELS.get(conf['log_level'], logging.INFO)
    root = logging.getLogger('')
    root.setLevel(level)
    cf = logging.Formatter(fmt=conf['log_fmt_console'], datefmt=conf['log_datefmt'])
    ch = logging.StreamHandler()
    ch.setLevel(level)
    ch.setFormatter(cf)
    root.addHandler(ch)
    ff = logging.Formatter(fmt=conf['log_fmt_console'], datefmt=conf['log_datefmt'])
    fh = logging.FileHandler(conf['log_file'])
    fh.setLevel(level)
    fh.setFormatter(ff)
    root.addHandler(fh)