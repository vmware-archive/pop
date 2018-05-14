# -*- coding: utf-8 -*-
# pylint: disable=expression-not-assigned

# Import third party libs
try:
    import tornado  # pylint: disable=unused-import
    HAS_TORNADO = True
except ImportError:
    HAS_TORNADO = False

# Import pack
import pop.hub


def test_asyncio_coro():
    hub = pop.hub.Hub()
    hub.tools.sub.add('mods', pypath='tests.mods.coro')
    assert 'coro' in hub.mods
    assert 'asyncio_demo' in dir(hub.mods.coro)
    try:
        hub.mods.coro.asyncio_demo()
    except Exception:
        raise


if HAS_TORNADO:
    def test_tornado_coro():
        hub = pop.hub.Hub()
        hub.tools.sub.add('mods', pypath='tests.mods.coro')
        assert 'coro' in hub.mods
        assert 'tornado_demo' in dir(hub.mods.coro)
        try:
            hub.mods.coro.tornado_demo()
        except Exception:
            raise
