# -*- coding: utf-8 -*-
'''
Control and add subsystems to the running daemon hub
'''
# Import pop libs
import pop.hub


def add(hub,
        modname,
        sub=None,
        subname=None,
        pypath=None,
        static=None,
        contracts_pypath=None,
        contracts_static=None,
        default_contracts=None,
        virtual=True,
        recurse=False,
        omit_start=('_'),
        omit_end=(),
        omit_func=False,
        omit_class=True,
        omit_vars=False,
        mod_basename='pop.sub',
        stop_on_failures=False,
        init=None,
        ):
    '''
    Add a new subsystem to the hub
    '''
    # Make sure that unintended funcs are not called with the init
    if init is True:
        init = 'init.new'
    subname = subname if subname else modname
    if sub:
        root = sub
    else:
        root = hub
    root._subs[modname] = pop.hub.Sub(
            hub,
            modname,
            subname,
            pypath,
            static,
            contracts_pypath,
            contracts_static,
            default_contracts,
            virtual,
            recurse,
            omit_start,
            omit_end,
            omit_func,
            omit_class,
            omit_vars,
            mod_basename,
            stop_on_failures)
    root._subs[modname]._pop_init(init)


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
    Load al modules under a given pop
    '''
    if hasattr(hub, subname):
        sub = getattr(hub, subname)
        sub._load_all()
        return True
    else:
        return False
