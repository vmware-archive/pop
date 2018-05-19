async def callback(hub, payload):
    if 'payload' in payload:
        hub.set_me = payload['payload']['ret']
    return 'foo'


async def ret(hub):
    await hub.proc.worker.ret({'ret': 'Returned'})
    return 'inline'
