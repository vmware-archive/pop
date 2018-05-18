# -*- coding: utf-8 -*-
'''
Find directories
'''
# Import python libs
import os
import importlib


def dir_list(pypath=None, static=None):
    '''
    Return the directories to look for modules in, pypath specifies files
    relative to an installed python package, static is for static dirs
    '''
    ret = []
    if pypath is None:
        pypath = []
    # pylint: disable=no-member
    if isinstance(pypath, str):
        pypath = pypath.split(',')
    if static is None:
        static = []
    if isinstance(static, str):
        static = static.split(',')
    # pylint: enable=no-member
    for path in pypath:
        mod = importlib.import_module(path)
        ret.append(os.path.dirname(mod.__file__))
    ret.extend(static)
    return ret
