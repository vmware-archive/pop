async def callback(hub, payload):
    if 'payload' in payload:
        hub.set_me = payload['payload']['ret']
    return 'foo'


async def ret(hub):
    await hub.proc.worker.ret({'ret': 'Returned'})
    return 'inline'


async def gen(hub, start, end):
    for x in range(start, end):
        yield x