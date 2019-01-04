# -*- coding: utf-8 -*-
'''
Find directories
'''
# Import python libs
import os
import importlib


def dir_list(subname, p_name, pypath=None, static=None, pyroot=None, staticroot=None):
    '''
    Return the directories to look for modules in, pypath specifies files
    relative to an installed python package, static is for static dirs
    '''
    ret = []
    for path in pypath:
        mod = importlib.import_module(path)
        ret.append(os.path.dirname(mod.__file__))
    for path in pyroot:
        p_full = f'{path}.{p_name}.{subname}'
        rmod = importlib.import_module(path)
        rfn = os.path.dirname(rmod.__file__)
        full = os.path.join(rfn, p_name, subname)
        py_full = os.path.join(full, '__init__.py')
        if os.path.isfile(py_full):
            mod = importlib.import_module(p_full)
            ret.append(os.path.dirname(mod.__file__))
    for path in staticroot:
        full = os.path.join(path, p_name, subname)
        if os.path.isdir(full):
            ret.append(full)
    ret.extend(static)
    return ret
