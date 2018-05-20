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
    await hub.proc.init.local_pool(3, name, hub.mods.proc.callback)
    await asyncio.sleep(1)  # Give the processes some time to spin up
    ret = await hub.proc.run.add_sub(name, 'mods', pypath='tests.mods')
    # Make sure we round robin all the procs a few times
    for ind in range(20):
        ret = await hub.proc.run.func(name, 'mods.test.ping')
        assert ret == {}
    ret_ret = await hub.proc.run.func(name, 'mods.proc.ret')
    assert hub.set_me == 'Returned'
    assert ret_ret == 'inline'


def test_create():
    hub = pop.hub.Hub()
    hub.opts = {}
    hub.opts['sock_dir'] = tempfile.mkdtemp()
    hub.tools.sub.add('proc', pypath='pop.mods.proc', init=True)
    hub.tools.sub.add('mods', pypath='tests.mods')
    hub.tools.loop.start(_test_create(hub))
