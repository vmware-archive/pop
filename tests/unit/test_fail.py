# -*- coding: utf-8 -*-
# pylint: disable=expression-not-assigned

# Import pytest
import pytest

# Import pop
import pop.exc
import pop.hub


def test_load_error():
    '''
    In this test, pop will continue loading although, when trying to
    access a functions which should be accessible on the module, a
    PopError is raised.
    '''
    hub = pop.hub.Hub()
    hub.pop.sub.add('tests.mods')
    with pytest.raises(pop.exc.PopError,
                       match='Failed to load bad'):
        hub.mods.bad.func()


def test_load_error_stop_on_failures():
    hub = pop.hub.Hub()
    hub.pop.sub.add(
        'tests.mods',
        stop_on_failures=True
    )
    with pytest.raises(pop.exc.PopError,
                       match='returned virtual error'):
        hub.mods.bad.func()['verror']


def _test_calling_load_error_raises_pop_error():
    '''
    In this test, pop will continue loading although, when trying to
    access a functions which should be accessible on the module, a
    PopError is raised.
    '''
    hub = pop.hub.Hub()
    hub.pop.sub.add(
        'tests.mods',
        stop_on_failures=True
    )
    with pytest.raises(pop.exc.PopError,
                       match='Failed to load python module'):
        hub.mods.bad_import.func()


def test_load_error_traceback_stop_on_failures():
    '''
    In this test case pop will simply stop processing when the error is found
    '''
    hub = pop.hub.Hub()
    hub.pop.sub.add(
            pypath='tests.mods.bad_import',
            subname='mods',
            stop_on_failures=True)
    with pytest.raises(pop.exc.PopError,
                       match='Failed to load python module'):
        hub.mods.bad_import.func()


def test_verror_does_not_overload_loaded_mod():
    '''
    This tests will load 2 mods under the vname virtualname, however, one of them
    will explicitly not load. This makes sure load errors to not shadow good mod loads
    '''
    hub = pop.hub.Hub()
    hub.pop.sub.add(
        pypath='tests.mods.same_vname',
        subname='mods',
    )
    assert hub.mods.vname.func() == 'wha? Yep!'


def _test_load_error_by_virtualname():
    '''
    This test will make sure that even that the module did not load, it can still be
    found under it's defined __virtualname__
    '''
    hub = pop.hub.Hub()
    hub.pop.sub.add(
        pypath='tests.mods',
        subname='mods',
    )
    with pytest.raises(pop.exc.PopError,
                       match='returned virtual error'):
        hub.mods.virtual_bad.func()

    with pytest.raises(pop.exc.PopLookupError,
                       match='Module "vbad" not found'):
        hub.mods.vbad.func()
