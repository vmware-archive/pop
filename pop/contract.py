# -*- coding: utf-8 -*-
'''
Contracts to enforce loader objects
'''

# Import python libs
import inspect
import os
from collections import namedtuple

# Import pop libs
import pop.exc


class ContractedContext(namedtuple('ContractedContext', ('func', 'args', 'kwargs', 'signature', 'ret', 'cache'))):
    '''
    Contracted function calling context
    '''
    def __new__(cls, func, args, kwargs, signature, ret=None, cache=None):  # pylint: disable=too-many-arguments
        if cache is None:
            cache = {}
        return super(ContractedContext, cls).__new__(cls, func, list(args), kwargs, signature, ret, cache)

    def get_argument(self, name):
        '''
        Return the value corresponding to a function argument after binding the contract context
        argument and keyword arguments to the function signature.
        '''
        return self.get_arguments()[name]

    def get_arguments(self):
        '''
        Return a dictionary of all arguments that will be passed to the function and their
        values, including default arguments.
        '''
        if '__bound_signature__' not in self.cache:
            try:
                self.cache['__bound_signature__'] = self.signature.bind(*self.args, **self.kwargs)
            except TypeError as e:
                for frame in inspect.trace():
                    if frame.function == 'bind' and frame.filename.endswith(os.sep+'inspect.py'):
                        raise pop.exc.BindError(e)
                raise
            # Apply any default values from the signature
            self.cache['__bound_signature__'].apply_defaults()
        return self.cache['__bound_signature__'].arguments


def load_contract(contracts, default_contracts, mod, name):
    '''
    return a Contract object loaded up
    '''
    raws = []
    if not contracts:
        return raws
    loaded_contracts = []
    if getattr(contracts, name):
        loaded_contracts.append(name)
        raws.append(getattr(contracts, name))
    if getattr(contracts, 'init'):
        loaded_contracts.append('init')
        raws.append(getattr(contracts, 'init'))
    if default_contracts:
        for contract in default_contracts:
            if contract in loaded_contracts:
                continue
            loaded_contracts.append(contract)
            raws.append(getattr(contracts, contract))
    if hasattr(mod, '__contracts__'):
        cnames = getattr(mod, '__contracts__')
        if not isinstance(cnames, (list, tuple)):
            cnames = cnames.split(',')
        for cname in cnames:
            if cname in contracts:
                if cname in loaded_contracts:
                    continue
                loaded_contracts.append(cname)
                raws.append(getattr(contracts, cname))
    return raws


def verify_contract(hub, raws, mod):  # pylint: disable=unused-argument
    '''
    Verify module level contract - functions only
    '''
    for raw in raws:
        if hasattr(raw, 'functions'):
            try:
                functions = raw.functions(mod)
            except TypeError:
                functions = raw.functions()
            for fun_name in functions:
                if not hasattr(mod, fun_name):
                    raise pop.exc.ContractModuleException(
                        'Missing function \'{}\' in {!r}'.format(fun_name, mod)
                    )
                func = getattr(mod, fun_name)
                if not callable(func):
                    raise pop.exc.ContractFuncException('{} is not a function'.format(fun_name))


class Wrapper:  # pylint: disable=too-few-public-methods
    def __init__(self, func, ref, name):
        self.func = func
        self.ref = ref
        self.name = name
        self.signature = inspect.signature(self.func)

    def __call__(self, *args, **kwargs):
        self.func(*args, **kwargs)

    def __repr__(self):
        return '<{} func={}.{}>'.format(self.__class__.__name__, self.func.__module__, self.name)


class Redirect(Wrapper):
    '''
    Replaces functions in loaded modules, so that direct calls (explicitly
    pass a hub) use the correct hub.
    '''
    def __call__(self, *args, **kwargs):
        # grab hub
        if args:
            hub = args[0]
            args = args[1:]
        else:
            for hub_name in self.signature.parameters:
                break
            hub = kwargs.pop(hub_name)
        # redirect the call to that hub
        return getattr(hub, f'{self.ref}.{self.name}')(*args, **kwargs)


class Contracted(Wrapper):  # pylint: disable=too-few-public-methods
    '''
    This class wraps functions that have a contract associated with them
    and executes the contract routines
    '''
    def __init__(self, hub, contracts, func, ref, name):
        super().__init__(func, ref, name)
        self.hub = hub
        self.contracts = contracts if contracts else []
        self._load_contracts()

    def _get_contracts_by_type(self, contract_type='pre'):
        matches = []

        fn_contract_name = '{}_{}'.format(contract_type, self.name)
        for contract in self.contracts:
            if hasattr(contract, fn_contract_name):
                matches.append(getattr(contract, fn_contract_name))
            if hasattr(contract, contract_type):
                matches.append(getattr(contract, contract_type))

        return matches

    def _load_contracts(self):
        self.contract_functions = {'pre': self._get_contracts_by_type('pre'),
                                   'call': self._get_contracts_by_type('call')[:1],
                                   'post': self._get_contracts_by_type('post')}
        self._has_contracts = sum([len(l) for l in self.contract_functions.values()]) > 0

    def __call__(self, *args, **kwargs):
        args = tuple([self.hub] + list(args))

        if not self._has_contracts:
            return self.func(*args, **kwargs)
        contract_context = ContractedContext(self.func, args, kwargs, self.signature)

        for fn in self.contract_functions['pre']:
            fn(contract_context)
        if self.contract_functions['call']:
            ret = self.contract_functions['call'][0](contract_context)
        else:
            ret = self.func(*args, **kwargs)
        for fn in self.contract_functions['post']:
            post_ret = fn(contract_context._replace(ret=ret))
            if post_ret is not None:
                ret = post_ret

        return ret
