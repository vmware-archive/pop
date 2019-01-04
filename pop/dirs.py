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
        full = os.path.join(path, p_name, subname)
        py_full = os.path.join(full, '__init__.py')
        if os.path.file(py_full):
            mod = importlib.import_module(path)
            ret.append(os.path.dirname(mod.__file__))
    for path in staticroot:
        full = os.path.join(path, p_name, subname)
        if os.path.isdir(full):
            ret.append(full)
    ret.extend(static)
    return ret
