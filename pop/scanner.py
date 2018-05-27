# -*- coding: utf-8 -*-
'''
Used to scan the given directories for loadable files
'''
# Import python libs
import os
import imp
import collections

PY_END = ('.py', '.pyc', '.pyo')
PYEXT_END = tuple([suffix[0] for suffix in imp.get_suffixes() if suffix[-1] == imp.C_EXTENSION])
CYTHON_END = ('.pyx',)
SKIP_DIRNAMES = ('__pycache__',)


def scan(dirs):
    '''
    Return a list of importable files
    '''
    ret = collections.OrderedDict()
    ret['python'] = collections.OrderedDict()
    ret['cython'] = collections.OrderedDict()
    ret['ext'] = collections.OrderedDict()
    ret['imp'] = collections.OrderedDict()
    for dir_ in dirs:
        for fn_ in os.listdir(dir_):
            _apply_scan(ret, dir_, fn_)
    return ret


def _apply_scan(ret, dir_, fn_):
    '''
    Convert the scan data into
    '''
    if fn_.startswith('_'):
        return
    if os.path.basename(dir_) in SKIP_DIRNAMES:
        return
    full = os.path.join(dir_, fn_)
    if '.' not in full:
        return
    bname = full[:full.rindex('.')]
    if fn_.endswith(PY_END):
        if bname not in ret['python']:
            ret['python'][bname] = {'path': full}
    if fn_.endswith(CYTHON_END):
        if bname not in ret['cython']:
            ret['cython'][bname] = {'path': full}
    if fn_.endswith(PYEXT_END):
        if bname not in ret['ext']:
            ret['ext'][bname] = {'path': full}
