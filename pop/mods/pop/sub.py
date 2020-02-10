# -*- coding: utf-8 -*-
'''
Control and add subsystems to the running daemon hub
'''
# Import python libs
import os
# Import pop libs
import pop.hub


def add(hub,
        pypath=None,
        subname=None,
        sub=None,
        static=None,
        contracts_pypath=None,
        contracts_static=None,
        default_contracts=None,
        virtual=True,
        dyne_name=None,
        omit_start=('_'),
        omit_end=(),
        omit_func=False,
        omit_class=True,
        omit_vars=False,
        mod_basename='pop.sub',
        stop_on_failures=False,
        init=True,
        ):
    '''
    Add a new subsystem to the hub
    '''
    if pypath:
        pypath = pop.hub.ex_path(pypath)
        subname = subname if subname else pypath[0].split('.')[-1]
    elif static:
        subname = subname if subname else os.path.basename(static)
    if dyne_name:
        subname = subname if subname else dyne_name
    if sub:
        root = sub
    else:
        root = hub
    root._subs[subname] = pop.hub.Sub(
            hub,
            subname,
            pypath,
            static,
            contracts_pypath,
            contracts_static,
            default_contracts,
            virtual,
            dyne_name,
            omit_start,
            omit_end,
            omit_func,
            omit_class,
            omit_vars,
            mod_basename,
            stop_on_failures)
    root._subs[subname]._sub_init(init)
    root._iter_subs = sorted(root._subs.keys())


def remove(hub, subname):
    '''
    Remove a pop from the hub, run the shutdown if needed
    '''
    if hasattr(hub, subname):
        sub = getattr(hub, subname)
        if hasattr(sub, 'init'):
            mod = getattr(sub, 'init')
            if hasattr(mod, 'shutdown'):
                mod.shutdown()
        hub._remove_subsystem(subname)


def load_all(hub, subname):
    '''
    Load all modules under a given pop
    '''
    if hasattr(hub, subname):
        sub = getattr(hub, subname)
        sub._load_all()
        return True
    else:
        return False


def get_dirs(hub, sub):
    '''
    Return a list of directories that contain the modules for this subname
    '''
    return sub._dirs


def iter_subs(hub, sub, recurse=False):
    '''
    Return an iterator that will traverse just the subs. This is useful for
    nested subs
    '''
    for name in sorted(sub._subs):
        ret = sub._subs[name]
        yield ret
        if recurse:
            if hasattr(ret, '_subs'):
                for nest in hub.pop.sub.iter_subs(ret, recurse):
                    yield nest


def load_subdirs(hub, sub, recurse=False):
    '''
    Given a sub, load all subdirectories found under the sub into a lower namespace
    '''
    dirs = hub.pop.sub.get_dirs(sub)
    roots = {}
    for dir_ in dirs:
        for fn in os.listdir(dir_):
            if fn.startswith('_'):
                continue
            if fn == 'contracts':
                continue
            full = os.path.join(dir_, fn)
            if not os.path.isdir(full):
                continue
            if fn not in roots:
                roots[fn] = [full]
            else:
                roots[fn].append(full)
    for name, sub_dirs in roots.items():
        # Load er up!
        hub.pop.sub.add(
                subname=name,
                sub=sub,
                static=sub_dirs,
                virtual=sub._virtual,
                omit_start=sub._omit_start,
                omit_end=sub._omit_end,
                omit_func=sub._omit_func,
                omit_class=sub._omit_class,
                omit_vars=sub._omit_vars,
                mod_basename=sub._mod_basename,
                stop_on_failures=sub._stop_on_failures)
        if recurse:
            hub.pop.sub.load_subdirs(getattr(sub, name), recurse)


def reload(hub, subname):
    '''
    Instruct the hub to reload the modules for the given sub. This does not call
    the init.new function or remove sub level variables. But it does re-read the
    directory list and re-initialize the loader causing all modules to be re-evaluated
    when started.
    '''
    if hasattr(hub, subname):
        sub = getattr(hub, subname)
        sub._prepare()
        return True
    else:
        return False


def extend(
        hub,
        subname,
        pypath=None,
        static=None,
        contracts_pypath=None,
        contracts_static=None):
    '''
    Extend the directory lookup for a given sub. Any of the directory lookup
    arguments can be passed.
    '''
    if not hasattr(hub, subname):
        return False
    sub = getattr(hub, subname)
    if pypath:
        sub._pypath.extend(pop.hub.ex_path(pypath))
    if static:
        sub._static.extend(pop.hub.ex_path(static))
    if contracts_pypath:
        sub._contracts_pypath.extend(pop.hub.ex_path(contracts_pypath))
    if contracts_static:
        sub._contracts_static.extend(pop.hub.ex_path(contracts_static))
    sub._prepare()
