'''
Subsystems are plugin interfaces, or plugin subsystems
'''


class Sub:
    '''
    The Sub is the object that creates the plugin reference object. All lookups
    are redirected to the correct modules loaded for the plugin subsystem
    '''
    def __init__(
            self,
            hub,
            name,
            pypath=None,
            dirpath=None,
            contracts_pypath=None,
            contracts_dirpath=None,
            virtual=True,
            recurse=True,
            omit_start=('_'),
            omit_end=(),
            omit_func=False,
            omit_class=False,
            omit_vars=False,
            mod_basename='pop.subs',
            init=None,
            ):
        self._hub = hub
        self._name = name
        self._mod_basename = mod_basename
        self._dirs = pop.dirs.dir_list(
                pypath,
                dirpath)
        self._contract_dirs = pop.dirs.dir_list(
                contracts_pypath,
                contracts_dirpath)
        if self._contract_dirs:
            self._contracts = Sub(
                    hub,
                    '{}.contracts'.format(name),
                    dirpath=self._contract_dirs)
        else:
            self._contracts = None
        self._default_contract = default_contract

