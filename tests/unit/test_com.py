# Import python libs
import os
# Import rosso libs
import pop.hub
# Import pytest
import pytest

CODE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))


def _setup():
    hub = pop.hub.Hub()
    hub.tools.sub.add('com', pypath='pop.mods.com', init=True)
    return hub


def test_connections():
    async def _test(hub):
        '''
        '''
        hub.com.pool.create('srv', hub.com.test.echo_router)
        # Yes we are maing sure port numbers can be strings or ints
        await hub.com.pool.add_con('srv', 'bind', '127.0.0.1', 65444)
        hub.com.pool.create('client', hub.com.test.echo_router)
        await hub.com.pool.add_con('client', 'client', '127.0.0.1', '65444')
        await hub.com.pool.add_con('client', 'client', '127.0.0.1', 65444)
        await hub.com.pool.add_con('client', 'client', '127.0.0.1', '65444')
        await hub.com.pool.add_con('client', 'client', '127.0.0.1', '65444')
        snd = 'no one expects the spanish inquisition'
        count = 0
        async for ret in hub.com.pool.pub('client', snd):
            count += 1
            assert ret == snd
        assert count == 4
        count = 0
        async for ret in hub.com.pool.pub('srv', snd):
            count += 1
            assert ret == snd
        assert count == 4
        assert snd == await hub.com.pool.rand('client', snd)
        assert snd == await hub.com.pool.rand('srv', snd)
        assert snd == await hub.com.pool.avail('client', snd)
        assert snd == await hub.com.pool.avail('srv', snd)
    hub = _setup()
    hub.tools.loop.start(_test(hub))