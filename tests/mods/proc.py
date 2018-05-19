
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


async def callback(hub, payload):
    print('Callback')
    if 'payload' in payload:
        hub.set_me = payload['payload']['ret']
    return 'foo'


async def ret(hub):
    await hub.proc.worker.ret({'ret': 'Returned'})
    return 'inline'
