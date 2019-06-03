# -*- coding: utf-8 -*-
'''
Provides tools to help unit test projects using pop.
For now, provides mock Hub instances.
'''
import inspect
import copy
from functools import partial
from asynctest.mock import create_autospec

from pop.contract import Contracted
from pop.loader import LoadedMod
from pop.hub import Hub, Sub


class _LookUpTable:
    def __init__(self, *args, **kwargs):
        self._lut = {}
        super().__init__(*args, **kwargs)

    def contains(self, key):
        return self.is_hashable(key) and key in self._lut

    def update(self, key, value):
        if self.is_hashable(key):
            self._lut[key] = value

    def lookup(self, key):
        return self._lut[key]

    def is_hashable(self, key):
        try:
            _ = {key: None}
            return True
        except TypeError:
            return False

    def __len__(self):
        return len(self._lut)


class _LazyPop:
    __lazy_classes = [Hub, Sub, LoadedMod]

    class __Lazy:
        pass

    def __init__(self, obj, lut=None):
        if isinstance(obj, Hub):
            lut = _LookUpTable()
            lut.update('hub', self)
            lut.update(obj, self)
        elif isinstance(obj, Sub):
            obj._load_all()

        self.__lut = lut
        self.__obj = obj
        for attr_name in self.__attr_names():
            setattr(self, attr_name, _LazyPop.__Lazy)

    def __attr_names(self):
        # TODO: '_' - is this actually right? what should I really expose?
        attrs = [attr for attr in self.__obj.__dict__ if not attr.startswith('_')]

        if isinstance(self.__obj, Hub):
            attrs += list(self.__obj._subs)
        elif isinstance(self.__obj, Sub):
            attrs += list(self.__obj._loaded)
            attrs += list(self.__obj._subs)
        elif isinstance(self.__obj, LoadedMod):
            attrs += list(self.__obj._attrs)
        else:
            raise Exception('Standard objects should not be lazy: {}'.format(str(self.__obj)))

        return attrs

    def __getattribute__(self, item):
        attr = super().__getattribute__(item)

        if attr is _LazyPop.__Lazy:
            orig = getattr(self.__obj, item)

            if self.__lut.contains(orig):
                attr = self.__lut.lookup(orig)
            elif [True for cls in self.__lazy_classes if isinstance(orig, cls)]:
                attr = self.__class__(orig, self.__lut)
            elif isinstance(orig, Contracted):
                attr = self._mock_function(orig)
            else:
                attr = self._mock_attr(orig)

            self.__lut.update(orig, attr)
            setattr(self, item, attr)

        return attr

    def _mock_attr(self, a):
        return create_autospec(a, spec_set=True)

    def _mock_function(self, f):
        raise NotImplementedError()


def strip_hub(f):
    '''
    returns a no-op function with the same function signature... minus the first parameter (hub).
    '''
    if inspect.iscoroutinefunction(f):
        newf = 'async '
    else:
        newf = ''
    newf += 'def {}('.format(f.__name__)
    params = inspect.signature(f).parameters
    new_params = []
    for param in params:
        if params[param].kind is inspect.Parameter.VAR_POSITIONAL:
            new_params.append('*{}'.format(param))
        elif params[param].kind is inspect.Parameter.VAR_KEYWORD:
            new_params.append('**{}'.format(param))
        else:
            new_params.append(param)
        if params[param].default is not inspect.Parameter.empty:
            new_params[-1] += '="has default"'
    newf += ', '.join(new_params[1:])  # skip hub
    newf += '): pass'

    scope = {}
    exec(newf, scope)

    return scope[f.__name__]


class MockHub(_LazyPop):
    '''
    Provides mocks mirroring a real hub::

        hub.sub.mod.fn()  # mock
        hub.sub.mod.attr  # mock
    '''
    def _mock_function(self, f):
        return create_autospec(strip_hub(f.func), spec_set=True)


class NoContractHub(_LazyPop):
    '''
    Provides access to real functions, bypassing contracts and mocking attributes::

        hub.sub.mod.fn()  # executes real function, no contracts
        hub.sub.mod.attr  # mock
    '''
    def _mock_function(self, f):
        return partial(f.func, self._LazyPop__lut.lookup('hub'))


class MockContracted:
    '''
    Creates a new contracted, but using a mock function.
    The mock function is masked to look just like the real function.

    Look up/set attributes first on the new contracted, then pass through to the mock.
    '''

    def __init__(self, c):
        mock_func = create_autospec(c.func, spec_set=True)
        mock_func.__module__ = c.func.__module__
        mock_func.__dict__.update(copy.deepcopy(c.func.__dict__))
        self.__dict__['contracted'] = Contracted(c.hub, c._mod, c.contracts, mock_func)
        self.signature = c.signature

    def __call__(self, *args, **kwargs):
        return self.contracted(*args, **kwargs)

    def __getattr__(self, attr):
        if attr in self.contracted.__dict__:
            # allow access to contracted variables
            return getattr(self.contracted, attr)
        else:
            # but pass through to mock functions otherwise
            return getattr(self.contracted.func, attr)

    def __setattr__(self, name, value):
        if name in self.contracted.__dict__:
            # allow access to contracted variables
            setattr(self.contracted, name, value)
        else:
            # but pass through to mock functions otherwise
            setattr(self.contracted.func, name, value)


class ContractHub(_LazyPop):
    '''
    Runs a call through the contract system, but the function is a mock. Mostly useful for integration tests:

        hub.sub.mod.fn()  # executes mock function, real contracts
        hub.sub.mod.attr  # mock

    You can verify what parameters are passed to a function after going through loaded contracts::

        contract_hub.sub.mod.fn('foo')
        assert contract_hub.sub.mod.fn.called_with('bar')

    --------------------------------

    You can view or modify the contracts that will be executed on one function for a test - but first:
    MODIFYING CONTRACTS THIS WAY IS NOT SAFE ON REAL HUBS AND OTHER TESTING HUB VARIANTS!

    I have previously thought of modifying contracts with mocks, only to realize what I really want is to
    unit test a specific contract. Think twice before using this functionality.

    --------------------------------

    The contract modules are visible via hub.sub.mod.fn.contracts, and the contract functions that will
    be called, wrapping fn are visible via hub.sub.mod.fn.contract_functions. It is safe to modify the
    contracts list or contract_functions dict only on a ContractHub.

    Examine that the first contract function to be called is 'foo.pre_fn', then bypass it::

        assert contract_hub.sub.mod.fn.contract_functions['pre'][0].__module__ is 'foo'
        assert contract_hub.sub.mod.fn.contract_functions['pre'][0].__name__ is 'pre_fn'
        hub.sub.mod.fn.contract_functions['pre'][0] = create_autospec(hub.sub.mod.fn.contract_functions['pre'][0])

    Assert that one contract will be called before another::

        assert contract_hub.sub.mod.fn.contracts.index(contract1) < contract_hub.sub.mod.fn.contracts.index(contract2)
    '''
    def _mock_function(self, f):
        return MockContracted(f)
