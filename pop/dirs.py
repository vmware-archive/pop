# -*- coding: utf-8 -*-
'''
Find directories
'''
# Import python libs
import os
import sys
import importlib


def dir_list(subname, p_name, pypath=None, static=None):
    '''
    Return the directories to look for modules in, pypath specifies files
    relative to an installed python package, static is for static dirs
    '''
    ret = []
    for path in pypath:
        mod = importlib.import_module(path)
        for m_path in mod.__path__:
            # If we are inside of an executable the path will be different
            ret.append(m_path)
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
        context = {}
        if not os.path.isfile(conf):
            continue
        try:
            with open(conf) as f:
                code = f.read()
                if  'DYNE' in code:
                    exec(code, context)
                else:
                    continue
        except Exception:
            continue
        if 'DYNE' in context:
            if not isinstance(context['DYNE'], dict):
                continue
            for name, paths in context['DYNE'].items():
                if not isinstance(paths, list):
                    continue
                if name not in ret:
                    ret[name] = []
                for path in paths:
                    ret[name].append(os.path.join(dir_, path.replace('.', os.sep)))
    return ret
