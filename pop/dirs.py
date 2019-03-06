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
        for path in mod.__path__:
            ret.append(path)
    for path in pyroot:
        p_full = f'{path}.{p_name}.{subname}'
        try:
            mod = importlib.import_module(p_full)
            for path in mod.__path__:
                ret.append(path)
        except ModuleNotFoundError:
            continue
    for path in staticroot:
        full = os.path.join(path, p_name, subname)
        if os.path.isdir(full):
            ret.append(full)
    ret.extend(static)
    return ret
