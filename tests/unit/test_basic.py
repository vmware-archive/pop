# -*- coding: utf-8 -*-
# pylint: disable=expression-not-assigned

# Import third party libs
import pytest

# Import pack
import pop.hub


def test_basic():
    hub = pop.hub.Hub()
    hub.tools.sub.add('tests.mods')
    hub.mods.test.ping()
    assert hub.mods.test.ping() == {}
    assert hub.mods.test.demo() is False
    assert hub.mods.test.ping() == hub.mods.foo.bar()


def test_getattr():
    hub = pop.hub.Hub()
    hub.tools.sub.add('tests.mods')
    hub.mods.test.ping()
    assert getattr(hub, 'mods.test.ping')() == {}
    assert getattr(hub.mods.test, 'demo')() is False
    assert hub.mods.test.ping() == getattr(hub, 'mods.foo.bar')()


def test_iter_sub():
    hub = pop.hub.Hub()
    hub.tools.sub.add('tests.mods')
    mods = []
    for mod in hub.mods:
        mods.append(mod.__sub_name__)
    assert mods == sorted(hub.mods._loaded.keys())


def test_iter_sub_nested():
    hub = pop.hub.Hub()
    hub.tools.sub.add('tests.mods')
    mods = []
    for _ in hub.mods:
        for mod in hub.mods:
            mods.append(mod.__sub_name__)
        break
    assert mods == sorted(hub.mods._loaded.keys())


def test_iter_hub():
    hub = pop.hub.Hub()
    hub.tools.sub.add('tests.mods')
    subs = []
    for sub in hub:
        subs.append(sub._subname)
    assert subs == sorted(hub._subs.keys())


def test_iter_hub_nested():
    hub = pop.hub.Hub()
    hub.tools.sub.add('tests.mods')
    subs = []
    for _ in hub:
        for sub in hub:
            subs.append(sub._subname)
        break
    assert subs == sorted(hub._subs.keys())


def test_iter_vars():
    hub = pop.hub.Hub()
    hub.tools.sub.add('tests.mods')
    funcs = []
    for var in hub.tools.sub:
        funcs.append(var.name)
    assert funcs == sorted(hub.tools.sub._funcs.keys())


def test_iter_vars_nested():
    hub = pop.hub.Hub()
    hub.tools.sub.add('tests.mods')
    funcs = []
    for _ in hub.tools.sub:
        for var in hub.tools.sub:
            funcs.append(var.name)
        break
    assert funcs == sorted(hub.tools.sub._funcs.keys())


def test_nest():
    '''
    Test the ability to nest the subs in a deeper namespace
    '''
    hub = pop.hub.Hub()
    hub.tools.sub.add('tests.mods')
    hub.tools.sub.add('tests.mods.nest', sub=hub.mods)
    assert hub.mods.nest.basic.ret_true()


def test_this():
    hub = pop.hub.Hub()
    hub.tools.sub.add('tests.mods')
    hub.mods.test.ping()
    assert hub.mods.test.this() == {}


def test_ref_sys():
    hub = pop.hub.Hub()
    hub.tools.sub.add('tests.mods')
    hub.mods.test.ping()
    assert hub.tools.ref.last('mods.test.ping')() == {}
    path = hub.tools.ref.path('mods.test.ping')
    assert len(path) == 4
    assert hasattr(path[0], 'mods')
    assert hasattr(path[1], 'test')
    assert hasattr(path[2], 'ping')
    rname = 'Made It!'
    hub.tools.ref.create('mods.test.Foo', rname)
    assert hub.mods.test.Foo == rname


def test_module_level_direct_call():
    hub = pop.hub.Hub()
    hub.tools.sub.add('tests.mods')
    with pytest.raises(Exception):
        hub.mods.test.module_level_non_aliased_ping_call()
    assert hub.mods.test.module_level_non_aliased_ping_call_fw_hub() == {}


def test_contract():
    hub = pop.hub.Hub()
    hub.tools.sub.add(
        'tests.mods',
        contracts_pypath='tests.contracts'
    )
    with pytest.raises(Exception) as context:
        hub.mods.test.ping(4)


def test_inline_contract():
    hub = pop.hub.Hub()
    hub.tools.sub.add('tests.cmods')
    assert hub.cmods.ctest.cping()
    assert hub.CPING


def test_no_contract():
    hub = pop.hub.Hub()
    hub.tools.sub.add('tests.mods')
    with pytest.raises(TypeError) as context:
        hub.mods.test.ping(4)


def test_contract_manipulate():
    hub = pop.hub.Hub()
    hub.tools.sub.add(
        'tests.mods',
        contracts_pypath='tests.contracts'
    )
    assert 'override' in hub.mods.all.list()
    assert 'post called' in hub.mods.all.list()
    assert 'post' in hub.mods.all.dict()


def test_private_function_cross_access():
    hub = pop.hub.Hub()
    hub.opts = 'OPTS!'
    hub.tools.sub.add('tests.mods')
    # Let's make sure that the private function is not accessible through
    # the packed module
    with pytest.raises(AttributeError) as exc:
        hub.mods.priv._private() == 'OPTS!'

    # Let's confirm that the private function has access to the cross
    # objects
    assert hub.mods.priv.public() == 'OPTS!'


def test_private_function_cross_access_with_contracts():
    hub = pop.hub.Hub()
    hub.opts = 'OPTS!'
    hub.tools.sub.add(
        'tests.mods',
        contracts_pypath='tests.contracts'
    )
    # Let's make sure that the private function is not accessible through
    # the packed module
    with pytest.raises(AttributeError) as exc:
        hub.mods.priv._private() == 'OPTS!'

    # Let's confirm that the private function has access to the cross
    # objects
    assert hub.mods.priv.public() == 'OPTS!'


def test_cross_in_virtual():
    hub = pop.hub.Hub()
    hub.opts = 'OPTS!'
    hub.tools.sub.add(
        'tests.mods',
        contracts_pypath='tests.contracts'
    )
    assert hub.mods.virt.present() is True


def test_virtual_ret_true():
    hub = pop.hub.Hub()
    hub.opts = 'OPTS!'
    hub.tools.sub.add(
        'tests.mods',
        contracts_pypath='tests.contracts'
    )
    assert hub.mods.truev.present() is True


def test_mod_init():
    hub = pop.hub.Hub()
    hub.context = {}
    hub.tools.sub.add(
        pypath='tests.mods.packinit',
        subname='mods',
        contracts_pypath='tests.contracts'
    )
    # Force load all to make sure mod is init'ed
    hub.mods._load_all()
    assert 'LOADED' in hub.context
    assert hub.mods.packinit.loaded() is True

    # Now without force loading, at least a function needs to be called
    hub = pop.hub.Hub()
    hub.context = {}
    hub.tools.sub.add(
        pypath='tests.mods.packinit',
        subname='mods',
        contracts_pypath='tests.contracts'
    )
    assert hub.context == {'NEW': True}
    assert 'LOADED' not in hub.context
    assert hub.mods.packinit.loaded() is True
    # And now __mod_init__ has been executed
    assert 'LOADED' in hub.context

    # don't run init
    hub = pop.hub.Hub()
    hub.context = {}
    hub.tools.sub.add(
        pypath='tests.mods.packinit',
        subname='mods',
        contracts_pypath='tests.contracts',
        init=False
    )
    assert hub.context == {}


def test_pack_init():
    hub = pop.hub.Hub()
    hub.context = {}
    hub.tools.sub.add(
        pypath='tests.mods.packinit',
        subname='mods',
        contracts_pypath='tests.contracts'
    )
    assert hub.mods.init.check() is True


def test_non_module_functions_are_not_packed():
    hub = pop.hub.Hub()
    hub.tools.sub.add('tests.mods')
    hub.mods._load_all()
    assert 'scan' not in dir(hub.mods.test)
    try:
        hub.mods.test.call_scan() is True
    except TypeError:
        pytest.fail('The imported \'scan\' function in \'tests.mods.test\' was wrongly packed')


def test_double_underscore():
    hub = pop.hub.Hub()
    hub.tools.sub.add('tests.mods')
    hub.mods.test.double_underscore()


def test_dyne():
    hub = pop.hub.Hub()
    hub.tools.sub.add(dyne_name='dyne1')
    assert hub.dyne1.INIT
    hub.tools.sub.add(dyne_name='dyne2')
    assert hub.dyne2.INIT
    hub.tools.sub.add(dyne_name='dyne3')
    assert hub.dyne3.INIT
    print(hub.dyne3.INIT)
    assert hub.dyne1.test.dyne_ping()
    assert hub.dyne1.nest.nest_dyne_ping()
    assert hub.dyne2.test.dyne_ping()
    assert hub.dyne2.nest.nest_dyne_ping()
    assert hub.dyne3.test.dyne_ping()
    assert hub.dyne3.nest.nest_dyne_ping()
