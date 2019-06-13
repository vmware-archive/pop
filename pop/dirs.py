# -*- coding: utf-8 -*-
'''
Find directories
'''
# Import python libs
import os
import sys
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


def inline_dirs(dirs, subdir):
    '''
    Look for the named subdir in the list of dirs
    '''
    ret = []
    for dir_ in dirs:
        check = os.path.join(dir_, subdir)
        if os.path.isdir(check):
            ret.append(check)
    return ret


def dynamic_dirs():
    '''
    Iterate over the available python package imports and look for configured
    dynamic dirs
    '''
    dirs = []
    ret = {}
    for dir_ in sys.path:
        if not os.path.isdir(dir_):
            continue
        for sub in os.listdir(dir_):
            full = os.path.join(dir_, sub)
            if full.endswith('.egg-link'):
                with open(full) as rfh:
                    dirs.append(rfh.read().strip())
            if os.path.isdir(full):
                dirs.append(full)
    for dir_ in dirs:
        conf = os.path.join(dir_, 'conf.py')
        if not os.path.isfile(conf):
            continue
        modname =f'{os.path.basename(dir_)}.conf'
        sfl = importlib.machinery.SourceFileLoader(modname, conf)
        cmod = sfl.load_module()
        if hasattr(cmod, 'DYNE'):
            for name, paths in cmod.DYNE.items():
                if name not in ret:
                    ret[name] = []
                for path in paths:
                    ret[name].append(os.path.join(dir_, path.replace('.', os.sep)))
    return ret
