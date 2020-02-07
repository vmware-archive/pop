# -*- coding: utf-8 -*-

from unittest.mock import sentinel, NonCallableMock, NonCallableMagicMock

import pytest

import pop.mods.pop.testing as testing
from pop.hub import Hub


class TestLazyPop:
    def test_lazy(self):
        hub = Hub()
        hub.pop.sub.add('tests.mods')

        # pylint: disable=pointless-statement
        l_hub = testing.MockHub(hub)
        assert len(l_hub._LazyPop__lut) == 2
        l_hub.mods
        assert len(l_hub._LazyPop__lut) == 3
        l_hub.mods.testing
        assert len(l_hub._LazyPop__lut) == 4
        l_hub.mods.testing.echo
        assert len(l_hub._LazyPop__lut) == 5

    def test_in_dict(self):
        # for autocompletion, all attributes should exist, even if it hasn't been called.
        hub = Hub()
        hub.pop.sub.add('tests.mods')

        l_hub = testing._LazyPop(hub)
        assert 'mods' in l_hub.__dict__

    def test_duplicate_object(self):
        hub = Hub()
        hub.pop.sub.add('tests.mods')

        hub.test_val = sentinel.test_val
        hub.mods.test_val = sentinel.test_val
        hub.mods.testing.test_val = sentinel.test_val

        l_hub = testing._LazyPop(hub)

        assert isinstance(l_hub.test_val, NonCallableMock)
        assert l_hub.test_val is l_hub.mods.test_val
        assert l_hub.mods.test_val is l_hub.mods.testing.test_val

    def test_duplicate_hub(self):
        hub = Hub()
        hub.pop.sub.add('tests.mods')

        hub.hub = hub
        hub.mods.hub = hub
        hub.mods.foo.hub = hub

        l_hub = testing._LazyPop(hub)

        assert l_hub.hub is l_hub
        assert l_hub.mods.hub is l_hub
        assert l_hub.mods.foo.hub is l_hub

    def test_recursive_subs(self):
        hub = Hub()
        hub.pop.sub.add('tests.mods')
        hub.pop.sub.add('tests.mods.nest', sub=hub.mods)
        l_hub = testing._LazyPop(hub)

        assert hub.mods.nest.basic.ret_true()

        with pytest.raises(NotImplementedError):
            l_hub.mods.nest.basic.ret_true()

    def test_var_exists_enforcement(self):
        hub = Hub()
        hub.pop.sub.add('tests.mods')

        hub.FOO = 'foo'
        hub.mods.FOO = 'foo'
        hub.mods.testing.FOO = 'foo'

        l_hub = testing._LazyPop(hub)

        for l in (l_hub, l_hub.mods, l_hub.mods.testing):
            try:
                assert isinstance(getattr(l, 'FOO'), NonCallableMagicMock)
            except Exception as e:
                raise type(e)('{}: {}'.format(type(l._LazyPop__obj).__name__, str(e)))
            with pytest.raises(AttributeError):
                l_hub.BAZ

    def test_recursive_get(self):
        hub = Hub()
        hub.pop.sub.add('tests.mods')
        assert hub.mods
        l_hub = testing._LazyPop(hub)

        result = getattr(l_hub, 'mods.foo')
        assert result is l_hub.mods.foo


class TestStripHub:
    def test_basic(self):
        def f(hub):
            pass
        g = testing.strip_hub(f)

        g()
        with pytest.raises(TypeError,
                           match=r'f\(\) takes 0 positional arguments'):
            g('bar')

    def test_param(self):
        def f(hub, foo):
            pass
        g = testing.strip_hub(f)

        g('foo')
        g(foo='foo')
        with pytest.raises(TypeError,
                           match=r'f\(\) missing 1 required positional'):
            g()

    def test_defaults(self):
        def f(hub, foo=None):
            pass
        g = testing.strip_hub(f)

        g()
        g('foo')
        g(foo='foo')

    def test_kwargs(self):
        def f(hub, arg, **kwargs):
            pass
        g = testing.strip_hub(f)

        g('arg')
        g('arg', kwarg1='arg1')
        g(arg='arg', kwarg1='arg1')

    def test_args(self):
        def f(hub, *args):
            pass
        g = testing.strip_hub(f)

        g()
        g('an arg')
        g('another arg')

    def test_keyword_only(self):
        def f(hub, *args, foo='foo'):
            pass
        g = testing.strip_hub(f)

        g('arg', foo='other foo')
        g(foo='other foo')
        with pytest.raises(TypeError,
                           match=r'f\(\) got an unexpected keyword argument'):
            g(baz='baz')


class TestMockHub:
    hub = Hub()
    hub.pop.sub.add('tests.mods')
    mock_hub = testing.MockHub(hub)

    def test_mock_hub_dereference_errors(self):
        with pytest.raises(AttributeError,
                           match="has no attribute 'nosub'"):
            self.mock_hub.nosub.nomodule.nofunc()

        with pytest.raises(AttributeError,
                           match="has no attribute 'nomodule'"):
            self.mock_hub.mods.nomodule.nofunc()

        with pytest.raises(AttributeError,
                           match="has no attribute 'nofunc'"):
            self.mock_hub.mods.testing.nofunc()

    def test_mock_hub_function_enforcement(self):
        with pytest.raises(TypeError,
                           match="missing a required argument: 'param'"):
            self.mock_hub.mods.testing.echo()

    def test_mock_hub_return_value(self):
        self.mock_hub.mods.testing.echo.return_value = sentinel.myreturn
        assert self.mock_hub.mods.testing.echo('param') is sentinel.myreturn

    @pytest.mark.asyncio
    async def test_async_echo(self):
        val = 'foo'
        assert await self.hub.mods.testing.async_echo(val) == val

        self.mock_hub.mods.testing.async_echo.return_value = val
        assert await self.mock_hub.mods.testing.async_echo(val + 'change') == val


class TestNoContractHub:
    hub = Hub()
    hub.pop.sub.add('tests.mods')
    nocontract_hub = testing.NoContractHub(hub)

    def test_call(self):
        val = self.nocontract_hub.mods.testing.echo(sentinel.param)
        assert val is sentinel.param


class TestMockContracted:
    hub = Hub()
    hub.pop.sub.add('tests.mods', contracts_pypath='tests.contracts')

    def test_hub_contract(self):
        assert self.hub.mods.testing.echo('foo') == 'contract foo'

    def test_contract_hub_contract(self):
        m_echo = testing.mock_contracted(self.hub.mods.testing.echo)
        m_echo.func.return_value = 'bar'
        assert m_echo('foo') == 'contract bar'

    def test_contract_hub_getattr(self):
        assert testing.mock_contracted(self.hub.mods.testing.echo).return_value

    def test_contract_hub_module(self):
        m_echo = testing.mock_contracted(self.hub.mods.testing.echo)
        func_module = self.hub.mods.testing.echo.func.__module__
        assert m_echo.func.__module__ == func_module

    def test_signature(self):
        m_sig = testing.mock_contracted(self.hub.mods.testing.signature_func)
        assert str(m_sig.signature) == "(hub, param1, param2='default')"

    def test_get_arguments(self):
        m_sig = testing.mock_contracted(self.hub.mods.testing.signature_func)
        m_sig('passed in')

    def test_copy_func_attributes(self):
        echo = testing.mock_contracted(self.hub.mods.testing.echo)
        attr_func = testing.mock_contracted(self.hub.mods.testing.attr_func)

        with pytest.raises(AttributeError):
            assert echo.func.test
        assert attr_func.func.test is True

        with pytest.raises(AttributeError):
            assert echo.func.__test__
        assert attr_func.func.__test__ is True


class TestContractHub:
    hub = Hub()
    hub.pop.sub.add('tests.mods', contracts_pypath='tests.contracts')
    contract_hub = testing.ContractHub(hub)

    def test_hub_contract(self):
        assert self.hub.mods.testing.echo('foo') == 'contract foo'

    def test_contract_hub_contract(self):
        assert isinstance(self.contract_hub.mods.testing.echo, testing.Contracted)

    @pytest.mark.asyncio
    async def test_async_echo(self):
        val = 'foo'
        expected = 'async contract ' + val
        assert await self.hub.mods.testing.async_echo(val) == expected

        self.contract_hub.mods.testing.async_echo.func.return_value = val
        assert await self.contract_hub.mods.testing.async_echo(val + 'change') == expected

    def test_contract_hub_inspect(self):
        # demo ways that we can inspect the contract system
        assert len(self.contract_hub.mods.testing.echo.contracts) == 1
        assert 'call_signature_func' in dir(self.contract_hub.mods.testing.echo.contracts[0])

    def test_contract_hub_modify(self):
        contract_hub = testing.ContractHub(self.hub)

        # modifying the contract
        contract_hub.mods.testing.echo.func.return_value = 'bar'
        assert contract_hub.mods.testing.echo('foo') == 'contract bar'
        contract_hub.mods.testing.echo.contract_functions['call'] = []
        assert contract_hub.mods.testing.echo('foo') == 'bar'

        # verify that modification didn't mess with the real hub:
        assert self.hub.mods.testing.echo('foo') == 'contract foo'
