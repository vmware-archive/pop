'''
Test the proc subsystem
'''
# Import python libs
import tempfile
# Import pop libs
import pop.hub

#    hub.tools.sub.add('mods', pypath='tests.mods')
#    hub.mods.test.ping()
#    assert hub.mods.test.ping() == {}
#    assert hub.mods.test.this_pack() == {}
#    assert hub.mods.test.demo() is False
#    assert hub.mods.test.ping() == hub.mods.foo.bar()


async def _test_create(hub):
    name = 'Tests'
    await hub.proc.init.local_pool(3, name)
    await hub.proc.run.add_sub(name, 'mods', pypath='tests.mods')
    ret = await hub.proc.run.func(name, 'mods.test.ping')
    assert ret == {}


def test_create():
    hub = pop.hub.Hub()
    hub.opts = {}
    hub.opts['sock_dir'] = tempfile.mkdtemp()
    hub.tools.sub.add('proc', pypath='pop.mods.proc', init=True)
    hub.tools.loop.start(_test_create(hub))
