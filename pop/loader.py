# -*- coding: utf-8 -*-
'''
Load the files detected from the scanner
'''
# Import Python libs
import os
import sys
import inspect
import logging
import tempfile
import importlib
import importlib.machinery
import imp as stdlib_imp
import traceback as stdlib_traceback

# Import 3rd-party libs
try:
    import pyximport
    HAS_CYTHON = True
except ImportError:
    HAS_CYTHON = False

# Import pop libs
import pop.exc
import pop.contract

log = logging.getLogger(__name__)


def _generate_module(name):
    '''
    Generate a module at runtime and insert it in sys.modules
    '''
    if name in sys.modules:
        return sys.modules[name]

    code = "'''POP sub auto generated parent module for {0}'''".format(name.split('.')[-1])
    module = stdlib_imp.new_module(name)
    exec(code, module.__dict__)  # pylint: disable=exec-used
    sys.modules[name] = module
    return module


def _populate_sys_modules(mod):
    '''
    This is a hack to populate sys.modules with the modules that pop loads
    while making sure that parent modules have the attribute for the child
    modules.
    '''
    mod_parts = mod.split('.')
    imp_mod = mod_parts.pop(0)
    gen_mod = _generate_module(imp_mod)
    while True:
        if not mod_parts:
            break
        part = mod_parts.pop(0)
        imp_mod += '.' + part
        gen_child_mod = _generate_module(imp_mod)
        setattr(gen_mod, part, gen_child_mod)
        gen_mod = gen_child_mod


class LoadError:
    '''
    Errors from the loader are contained herein
    '''
    __slots__ = ('edict', 'traceback')

    def __init__(self, msg, exception=None, traceback=None, verror=None):
        self.edict = {
                'msg': msg,
                'exception': exception,
                'verror': verror,
                }
        self.traceback = traceback

    def __call__(self):
        '''
        Return the error cases
        '''
        return self.edict

    def __getattr__(self, attr):
        '''
        Return a lambda that returns the edict
        '''
        return self.__calling_load_error__

    def __calling_load_error__(self, *args, **kwargs):  # pylint: disable=unused-argument
        if self.edict['verror']:
            error = '{0[msg]}: {0[verror]}'.format(self())
            raise pop.exc.PopError(error)
        error = '{0[msg]}: {0[exception]!r}'.format(self())
        if self.traceback:
            error += '\n' + self.traceback
        raise pop.exc.PopError(error)

    def __repr__(self):
        return '<{} edict={!r}>'.format(self.__class__.__name__, self.edict)


def load_all(modname, scan):
    '''
    Load the modules from the scanner
    '''
    this = sys.modules[__name__]
    mods = {}
    for fname in scan:
        func = getattr(this, fname)
        for bname in scan[fname]:
            for path in scan[fname][bname]:
                mods[bname] = func(modname, path)
    return mods


def load_mod(modname, form, path, parent):
    '''
    Load a single module
    '''
    this = sys.modules[__name__]
    return getattr(this, form)(modname, path, parent)


def ext(modname, path, parent):
    '''
    Attempt to load the named python modules
    '''
    modname = '.'.join(modname.split('.')[:-1])
    _populate_sys_modules(modname)
    try:
        return stdlib_imp.load_dynamic(modname, path)
    except Exception as exc:  # pylint: disable=broad-except
        return LoadError(
                'Failed to load python module {} at path {}'.format(modname, path),
                exception=exc,
                traceback=stdlib_traceback.format_exc())


def python(modname, path, parent):
    '''
    Attempt to load the named python modules
    '''
    try:
        if not hasattr(importlib.machinery, "SourceFileLoader"):
            return stdlib_imp.load_source(modname, path)
        else:
            sfl = importlib.machinery.SourceFileLoader(modname, path)
            return sfl.load_module()
    except Exception as exc:  # pylint: disable=broad-except
        return LoadError(
                'Failed to load python module {} at path {}'.format(modname, path),
                exception=exc,
                traceback=stdlib_traceback.format_exc())


def cython(modname, path, parent):
    '''
    Import cython module
    '''
    if not HAS_CYTHON:
        try:
            raise ImportError('Cython not available')
        except ImportError as exc:
            return exc
    try:
        return pyximport.load_module(
                modname,
                path,
                tempfile.gettempdir())
    except Exception as exc:  # pylint: disable=broad-except
        return LoadError(
                'Failed to load cython module {} at path {}'.format(modname, path),
                exception=exc,
                traceback=stdlib_traceback.format_exc())


def imp(modname, path, parent):
    '''
    Import "static path" modules
    '''
    try:
        top_mod = __import__(path, globals(), locals(), [])
    except Exception as exc:  # pylint: disable=broad-except
        return LoadError(
                'Failed to load module {} at path {}'.format(modname, path),
                exception=exc,
                traceback=stdlib_traceback.format_exc())
    comps = path.split('.')
    if len(comps) < 2:
        mod = top_mod
    else:
        mod = top_mod
        for subname in comps[1:]:
            mod = getattr(mod, subname)
    sys.modules[modname] = mod
    # Clean up path from sys.modules
    del sys.modules[path]

    return mod


def load_virtual(parent, virtual, mod, bname):
    '''
    Run the virtual function to name the module and check for all loader
    errors
    '''
    base_name = os.path.basename(bname)
    if '.' in base_name:
        base_name = base_name.split('.')[0]
    try:
        name = mod.__virtualname__
    except Exception:  # pylint: disable=broad-except
        name = base_name
    if isinstance(mod, LoadError):
        # The mod is a LoadError instance.
        # Return the load error with name as the base_name because another
        # module is still allowed to load under the same __virtualname__
        # but also return the vname information
        return {'name': base_name, 'vname': name, 'error': mod}

    if not virtual:
        # __virtual__ is not to be processed. Return now!
        return {'name': base_name}

    if not hasattr(mod, '__virtual__'):
        # No __virtual__ processing is required.
        # Return the mod's name as the defined __virtualname__ if defined,
        # else, the base_name
        return {'name': name}

    try:
        vret = mod.__virtual__(parent)
    except Exception as exc:  # pylint: disable=broad-except
        err = LoadError(
                'Virtual threw exception in mod {}'.format(bname),
                exception=exc,
                traceback=stdlib_traceback.format_exc())
        # Return the load error with name as the base_name because another
        # module is still allowed to load under the same __virtualname__
        # but also return the vname information
        return {'name': base_name, 'vname': name, 'error': err}

    if vret is True:
        # No problems occurred, module is allowed to load
        # Return the mod's name as the defined __virtualname__ if defined,
        # else, the base_name
        return {'name': name}

    if vret is False:
        # __virtual__ explicitly disabled the loading of this module
        err = LoadError(
                'Module {} returned virtual FALSE'.format(bname),
                verror=vret)
        # Return the load error with name as the base_name because another
        # module is still allowed to load under the same __virtualname__
        # but also return the vname information
        return {'name': base_name, 'vname': name, 'error': err}

    # Anything else besides True/False should be considered a LoadError
    err = LoadError(
            'Module {} returned virtual error'.format(bname),
            verror=vret)
    # Return the load error with name as the base_name because another
    # module is still allowed to load under the same __virtualname__
    # but also return the vname information
    return {'name': base_name, 'vname': name, 'error': err}


def mod_init(parent, mod):
    '''
    Process module's __mod_init__ function if one if defined
    '''
    if hasattr(mod, '__mod_init__'):
        mod.__mod_init__(parent)


def prep_mod_dict(this_pack, mod, pack_name, contracts, loading_contract_sub=False):
    '''
    Read the attributes of the loaded module and remap them and omit objects
    that should not be exposed
    '''
    # pylint: disable=protected-access
    mod_dict = LoadedMod(pack_name)
    for attr in getattr(mod, '__load__', dir(mod)):
        name = getattr(mod, '__func_alias__', {}).get(attr, attr)
        func = getattr(mod, attr)
        if not this_pack._omit_vars:
            if not inspect.isfunction(func) and not inspect.isclass(func) and \
                    type(func).__name__ != 'cython_function_or_method':
                mod_dict._vars[name] = func
                mod_dict._attrs[name] = func
                continue
        if attr.startswith(this_pack._omit_start):
            continue
        if attr.endswith(this_pack._omit_end):
            continue
        if inspect.isfunction(func) or inspect.isbuiltin(func) or \
                type(func).__name__ == 'cython_function_or_method':
            obj = pop.contract.Contracted(this_pack._hub, mod_dict, contracts, func)
            if not this_pack._omit_func:
                if this_pack._pypath and not func.__module__.startswith(mod.__name__):
                    # We're only interested in functions defined in this module, not
                    # imported functions
                    continue
                mod_dict._funcs[name] = obj
                mod_dict._attrs[name] = obj
                if loading_contract_sub is False:
                    # Allow the function to be called directly from within the module while
                    # not breaking out of contracts. The original function name, not the aliased one
                    # or we'd risk overwriting python keywords, etc...
                    setattr(sys.modules[mod.__name__], attr, obj)
        else:
            klass = func
            if not this_pack._omit_class and inspect.isclass(klass):
                if not klass.__module__.startswith((this_pack._pypath, mod.__name__)):
                    # We're only interested in classes defined in this module, not
                    # imported classes
                    continue
                mod_dict._classes[name] = klass
                mod_dict._attrs[name] = klass
    return mod_dict


class LoadedMod:
    '''
    The LoadedMod class allows for the module loaded onto the sub to return
    custom sequencing, for instance it can be iterated over to return all
    functions
    '''
    def __init__(self, name):
        self.__sub_name__ = name
        self._vars = {}
        self._funcs = {}
        self._classes = {}
        self._attrs = {}

    def __getattr__(self, item):
        if item in self._attrs:
            return self._attrs[item]
        raise AttributeError(item)

    def __iter__(self):
        keys = sorted(self._funcs)
        ret = []
        for key in keys:
            ret.append(self._funcs[key])
        return iter(ret)

    def __dir__(self):
        # TODO: This should return finite set attrs as well as dunder attrs
        ret = list(self._attrs.keys())
        ret.extend(['__name__', '_vars', '_funcs', '_classes', '_attrs'])
        return ret
