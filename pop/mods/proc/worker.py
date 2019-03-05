'''
This module is used to manage the process started up by the pool. Work in this
module is used to manage the worker process itself and not other routines on
the hub this process was derived from

This is an exec, not a fork! This is a fresh memory space!
'''
# Import python libs
import os
import types
import asyncio
# Import third party libs
import msgpack
# TODO: The workers should detect if thier controlling process dies and terminate by themselves
# The controlling process will kill them when it exists, but if it exists hard then the workers
# Should be able to also clean themselves up


def start(hub, sock_dir, ind, ref, ret_ref):
    '''
    This funtion is called by the startup script to create a worker process

    :NOTE: This is a new process started from the shell, it does not have any
    of the process namespace from the creating process.
    This is an EXEC, NOT a FORK!
    '''
    hub.proc.SOCK_DIR = sock_dir
    hub.proc.REF = ref
    hub.proc.SOCK_PATH = os.path.join(sock_dir, ref)
    hub.proc.RET_REF = ret_ref
    hub.proc.RET_SOCK_PATH = os.path.join(sock_dir, ret_ref)
    hub.proc.IND = ind
    hub.tools.loop.start(hub.proc.worker.hold(), hub.proc.worker.server())


async def hold(hub):
    '''
    This function just holds the loop open by sleeping in a while loop
    '''
    while True:
        await asyncio.sleep(60)


async def server(hub):
    '''
    Start the unix socket server to recive commands
    '''
    await asyncio.start_unix_server(
            hub.proc.worker.work,
            path=hub.proc.SOCK_PATH)


async def work(hub, reader, writer):
    '''
    Process the incomming work
    '''
    inbound = await reader.readuntil(hub.proc.DELIM)
    inbound = inbound[:-len(hub.proc.DELIM)]
    payload = msgpack.loads(inbound, encoding='utf8')
    ret = b''
    if 'fun' not in payload:
        ret = {'err': 'Invalid format'}
    elif payload['fun'] == 'sub':
        # Time to add a sub to the hub!
        try:
            hub.proc.worker.add_sub(payload)
            ret = {'status': True}
        except Exception as exc:
            ret = {'status': False, 'exc': str(exc)}
    elif payload['fun'] == 'run':
        # Time to do some work!
        try:
            ret = await hub.proc.worker.run(payload)
        except Exception as exc:
            ret = {'status': False, 'exc': str(exc)}
    elif payload['fun'] == 'gen':
        ret = await hub.proc.worker.gen(payload, reader, writer)
    ret = msgpack.dumps(ret, use_bin_type=True)
    ret += hub.proc.D_FLAG
    ret += hub.proc.DELIM
    writer.write(ret)
    await writer.drain()
    writer.close()


def add_sub(hub, payload):
    '''
    Add a new sub onto the hub for this worker
    '''
    hub.tools.sub.add(*payload['args'], **payload['kwargs'])


async def gen(hub, payload, reader, writer):
    '''
    Run a generator and yield back the returns. Supports a generator and an
    async generator
    '''
    ref = payload.get('ref')
    args = payload.get('args', [])
    kwargs = payload.get('kwargs', {})
    ret = hub.tools.ref.last(ref)(*args, **kwargs)
    if isinstance(ret, types.AsyncGeneratorType):
        async for chunk in ret:
            rchunk = msgpack.dumps(chunk, use_bin_type=True)
            rchunk += hub.proc.I_FLAG
            rchunk += hub.proc.DELIM
            writer.write(rchunk)
            await writer.drain()
    elif isinstance(ret, types.GeneratorType):
        for chunk in ret:
            rchunk = msgpack.dumps(chunk, use_bin_type=True)
            rchunk += hub.proc.I_FLAG
            rchunk += hub.proc.DELIM
            writer.write(rchunk)
            await writer.drain()
    elif asyncio.iscoroutine(ret):
        return await ret
    else:
        return ret
    return ''


async def run(hub, payload):
    '''
    Execute the given payload
    '''
    ref = payload.get('ref')
    args = payload.get('args', [])
    kwargs = payload.get('kwargs', {})
    ret = hub.tools.ref.last(ref)(*args, **kwargs)
    if asyncio.iscoroutine(ret):
        return await ret
    return ret


async def ret(hub, payload):
    '''
    Send a return payload to the spawning process. This return will be tagged
    with the index of the process that returned it
    '''
    payload = {'ind': hub.proc.IND, 'payload': payload}
    mp = msgpack.dumps(payload, use_bin_type=True)
    mp += hub.proc.DELIM
    reader, writer = await asyncio.open_unix_connection(path=hub.proc.RET_SOCK_PATH)
    writer.write(mp)
    await writer.drain()
    ret = await reader.readuntil(hub.proc.DELIM)
    ret = ret[:-len(hub.proc.DELIM)]
    writer.close()
    return msgpack.loads(ret, encoding='utf8')
