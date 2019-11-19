# Import python libs
import logging


def setup(hub, conf):
    '''
    Given the configuration data set up the logger
    '''
    level = hub.conf.log.LEVELS.get(conf['log_level'], logging.INFO)
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
