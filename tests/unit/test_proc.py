'''
Test the proc subsystem
'''
# Import python libs
import asyncio
import tempfile
import os
# Import pop libs
import pop.hub


async def _test_create(hub):
    name = 'Tests'
    await hub.proc.init.pool(3, name, hub.mods.proc.callback, tempfile.mkdtemp())
    #await asyncio.sleep(1)  # Give the processes some time to spin up
    ret = await hub.proc.run.add_sub(name, 'mods', pypath='tests.mods')
    # Make sure we round robin all the procs a few times
    for ind in range(20):
        ret = await hub.proc.run.func(name, 'mods.test.ping')
        assert ret == {}
    ret_ret = await hub.proc.run.func(name, 'mods.proc.ret')
    assert hub.set_me == 'Returned'
    assert ret_ret == 'inline'

    # Test iterator systems
    n = []
    s = []
    e = []
    async for ind in hub.proc.run.gen(name, 'mods.proc.gen', 23, 77):
        n.append(ind)
    for ind in range(23, 77):
        e.append(ind)
    assert n == e
    async for ind in hub.proc.run.gen(name, 'mods.proc.simple_gen', 23, 77):
        s.append(ind)
    assert s == e
    # Test pub
    assert await hub.proc.run.pub(name, 'mods.proc.init_lasts')

    # Test track and ind func calls
    ind, coro = await hub.proc.run.track_func(name, 'mods.proc.echo_last')
    last_1, next_1 = await coro
    for _ in range(5):
        last_2, next_2 = await hub.proc.run.ind_func(name, ind, 'mods.proc.echo_last')
        assert next_1 == last_2
        next_1 = next_2
    # Test gen_track and ind_gen
    last_1, next_1 = await hub.proc.run.ind_func(name, ind, 'mods.proc.echo_last')
    for _ in range(5):
        async for last_2, next_2 in hub.proc.run.ind_gen(name, ind, 'mods.proc.gen_last'):
            assert next_1 == last_2
            next_1 = next_2

    # Test add_proc
    pre = len(hub.proc.Workers[name])
    await hub.proc.run.add_proc(name)
    post = len(hub.proc.Workers[name])
    assert pre < post
    for _ in range(20):
        ret = await hub.proc.run.func(name, 'mods.test.ping')


def test_create():
    hub = pop.hub.Hub()
    hub.opts = {}
    hub.tools.sub.add('proc', pypath='pop.mods.proc', init=True)
    hub.tools.sub.add('mods', pypath='tests.mods')
    hub.tools.loop.start(_test_create(hub))
