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
    hub.tools.sub.add(
            'mods',
            pypath='tests.mods',)
    with pytest.raises(pop.exc.PopError) as exc:
        hub.mods.bad.func()
    assert 'Failed to load bad' in str(exc)


def test_load_error_stop_on_failures():
    hub = pop.hub.Hub()
    hub.tools.sub.add(
            'mods',
            pypath='tests.mods',
            stop_on_failures=True)
    with pytest.raises(pop.exc.PopError) as exc:
        hub.mods.bad.func()['verror']
    assert 'returned virtual error' in str(exc)


def _test_calling_load_error_raises_pop_error():
    '''
    In this test, pop will continue loading although, when trying to
    access a functions which should be accessible on the module, a
    PopError is raised.
    '''
    hub = pop.hub.Hub()
    hub.tools.sub.add(
            'mods',
            pypath='tests.mods',
            stop_on_failures=True)
    with pytest.raises(pop.exc.PopError) as exc:
        hub.mods.bad_import.func()
    assert 'Failed to load python module' in str(exc)


def test_load_error_traceback_stop_on_failures():
    '''
    In this test case pop will simply stop processing when the error is found
    '''
    hub = pop.hub.Hub()
    hub.tools.sub.add(
            'mods',
            pypath='tests.mods.bad_import',
            stop_on_failures=True)
    with pytest.raises(pop.exc.PopError) as exc:
        hub.mods.bad_import.func()
    assert 'Failed to load python module' in str(exc)


def test_verror_does_not_overload_loaded_mod():
    '''
    This tests will load 2 mods under the vname virtualname, however, one of them
    will explicitly not load. This makes sure load errors to not shadow good mod loads
    '''
    hub = pop.hub.Hub()
    hub.tools.sub.add(
            'mods',
            pypath='tests.mods.same_vname',
    )
    assert hub.mods.vname.func() == 'wha? Yep!'


def _test_load_error_by_virtualname():
    '''
    This test will make sure that even that the module did not load, it can still be
    found under it's defined __virtualname__
    '''
    hub = pop.hub.Hub()
    hub.tools.sub.add(
            'mods',
            pypath='tests.mods',)
    with pytest.raises(pop.exc.PopError) as exc:
        hub.mods.virtual_bad.func()
    assert 'returned virtual error' in str(exc)

    with pytest.raises(pop.exc.PopLookupError) as exc:
        hub.mods.vbad.func()
    assert 'Module "vbad" not found' in str(exc)
