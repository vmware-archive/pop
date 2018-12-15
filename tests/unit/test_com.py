# Import python libs
import os
import tempfile
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
        async for ret in hub.com.pool.rand('client', snd):
            assert ret == snd
        async for ret in hub.com.pool.rand('srv', snd):
            assert ret == snd
        async for ret in hub.com.pool.avail('client', snd):
            assert ret == snd
        async for ret in hub.com.pool.avail('srv', snd):
            assert ret == snd
    hub = _setup()
    hub.tools.loop.start(_test(hub))


def test_unix():
    async def _test(hub):
        hub.com.pool.create('srv', hub.com.test.echo_router)
        hub.com.pool.create('client', hub.com.test.echo_router)
        path = os.path.join(tempfile.gettempdir(), os.urandom(8).hex())
        await hub.com.pool.add_unix_con('srv', 'bind', path)
        await hub.com.pool.add_unix_con('client', 'client', path)
        await hub.com.pool.add_unix_con('client', 'client', path)
        await hub.com.pool.add_unix_con('client', 'client', path)
        await hub.com.pool.add_unix_con('client', 'client', path)
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
        async for ret in hub.com.pool.rand('client', snd):
            assert ret == snd
        async for ret in hub.com.pool.rand('srv', snd):
            assert ret == snd
        async for ret in hub.com.pool.avail('client', snd):
            assert ret == snd
        async for ret in hub.com.pool.avail('srv', snd):
            assert ret == snd
    hub = _setup()
    hub.tools.loop.start(_test(hub))


def test_mixed():
    async def _test(hub):
        hub.com.pool.create('srv', hub.com.test.echo_router)
        hub.com.pool.create('client', hub.com.test.echo_router)
        path = os.path.join(tempfile.gettempdir(), os.urandom(8).hex())
        await hub.com.pool.add_unix_con('srv', 'bind', path)
        await hub.com.pool.add_unix_con('client', 'client', path)
        await hub.com.pool.add_unix_con('client', 'client', path)
        await hub.com.pool.add_unix_con('client', 'client', path)
        await hub.com.pool.add_unix_con('client', 'client', path)
        # Yes we are maing sure port numbers can be strings or ints
        await hub.com.pool.add_con('srv', 'bind', '127.0.0.1', 65445)
        await hub.com.pool.add_con('client', 'client', '127.0.0.1', '65445')
        await hub.com.pool.add_con('client', 'client', '127.0.0.1', 65445)
        await hub.com.pool.add_con('client', 'client', '127.0.0.1', '65445')
        await hub.com.pool.add_con('client', 'client', '127.0.0.1', '65445')
        snd = 'no one expects the spanish inquisition'
        count = 0
        async for ret in hub.com.pool.pub('client', snd):
            count += 1
            assert ret == snd
        assert count == 8
        count = 0
        async for ret in hub.com.pool.pub('srv', snd):
            count += 1
            assert ret == snd
        assert count == 8
        async for ret in hub.com.pool.rand('client', snd):
            assert ret == snd
        async for ret in hub.com.pool.rand('srv', snd):
            assert ret == snd
        async for ret in hub.com.pool.avail('client', snd):
            assert ret == snd
        async for ret in hub.com.pool.avail('srv', snd):
            assert ret == snd
    hub = _setup()
    hub.tools.loop.start(_test(hub))


def test_tgt():
    async def _test(hub):
        '''
        '''
        hub.com.pool.create('srv', hub.com.test.echo_router)
        # Yes we are making sure port numbers can be strings or ints
        await hub.com.pool.add_con('srv', 'bind', '127.0.0.1', 65446, {'id': 's1'})
        hub.com.pool.create('client', hub.com.test.echo_router)
        await hub.com.pool.add_con('client', 'client', '127.0.0.1', '65446', {'id': 'c1'})
        await hub.com.pool.add_con('client', 'client', '127.0.0.1', 65446, {'id': 'c2'})
        await hub.com.pool.add_con('client', 'client', '127.0.0.1', '65446', {'id': 'c3', 'grains': {'os': 'Arch'}})
        await hub.com.pool.add_con('client', 'client', '127.0.0.1', '65446', {'id': 'c4', 'grains': {'os': 'Arch'}})
        snd = 'no one expects the spanish inquisition'
        count = 0
        print(hub.com.POOLS['srv'])
        async for ret in hub.com.pool.tgt('srv', snd, 'glob', {'id': 'c*'}):
            count += 1
            assert ret == snd
        assert count == 4
        count = 0
        async for ret in hub.com.pool.tgt('srv', snd, 'match', {'grains': 'Arch'}):
            count += 1
            assert ret == snd
        assert count == 2

    hub = _setup()
    hub.tools.loop.start(_test(hub))
