# -*- coding: utf-8 -*-
'''
Contracts to enforce loader objects
'''

# Import python libs
import inspect
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
        Get the passed argument name value after binding the contract context argument and
        keyword arguments to the function signature.
        '''
        if '__bound_signature__' not in self.cache:
            self.cache['__bound_signature__'] = self.signature.bind(*self.args, **self.kwargs)
        return self.cache['__bound_signature__'].arguments[name]


def load_contract(contracts, default_contracts, mod):
    '''
    return a Contract object loaded up
    '''
    raws = []
    if not contracts:
        return raws
    loaded_contracts = []
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


def verify_contract(parent, raws, mod):  # pylint: disable=unused-argument
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


class Contracted:  # pylint: disable=too-few-public-methods
    '''
    This class wraps functions that have a contract associated with them
    and executes the contract routines
    '''
    def __init__(self, parent, contracts, func):
        self.parent = parent
        self.contracts = contracts if contracts else []
        self.func = func
        self.func_name = func.__name__
        self.__name__ = func.__name__
        self.signature = inspect.signature(self.func)

    def __call__(self, *args, **kwargs):  # pylint: disable=too-many-branches
        if args and (args[0] is self.parent or isinstance(args[0], self.parent.__class__)):
            # The hub(parent) is being passed directly, remove it from args
            # since we'll inject it further down
            args = list(args)[1:]
        args = tuple([self.parent] + list(args))
        if not self.contracts:
            return self.func(*args, **kwargs)
        contract_context = ContractedContext(self.func, args, kwargs, self.signature)
        pre = 'pre_{}'.format(self.func_name)
        post = 'post_{}'.format(self.func_name)
        call = 'call_{}'.format(self.func_name)
        # Build the context containing the function to call, the arguments and
        # the keyword arguments. This context can also be used to pass data
        # between the pre/call/post steps.
        for contract in self.contracts:
            if hasattr(contract, pre):
                getattr(contract, pre)(contract_context)
            if hasattr(contract, 'pre'):
                getattr(contract, 'pre')(contract_context)
        if self.contracts:
            if hasattr(self.contracts[0], call):
                ret = getattr(self.contracts[0], call)(contract_context)
            elif hasattr(self.contracts[0], 'call'):
                ret = getattr(self.contracts[0], 'call')(contract_context)
            else:
                ret = self.func(*args, **kwargs)
        else:
            ret = self.func(*args, **kwargs)
        for contract in self.contracts:
            if hasattr(contract, post):
                post_func = getattr(contract, post)
            elif hasattr(contract, 'post'):
                post_func = getattr(contract, 'post')
            else:
                post_func = None
            if post_func is not None:
                post_ret = post_func(contract_context._replace(ret=ret))
                if post_ret is not None:
                    ret = post_ret
        return ret

    def __repr__(self):
        return '<{} func={}.{}>'.format(self.__class__.__name__, self.func.__module__, self.func.__name__)
