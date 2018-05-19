'''
Execute functions or load subs on the workers in the named worker pool
'''
# import python libs
import asyncio
# Import third party libs
import msgpack


async def add_sub(hub, worker_name, *args, **kwargs):
    '''
    Tell all of the worker in the named pool to load the given sub,

    This funtion takes all of the same arguments as hub.tools.sub.add
    '''
    ret = {}
    workers = hub.proc.Workers[worker_name]
    for ind in workers:
        payload = {'fun': 'sub', 'args': args, 'kwargs': kwargs}
        # TODO: Make these futures to the run at the same time
        ret[ind] = await hub.proc.run.send(workers[ind], payload)
    return ret


async def pub(hub, worker_name, func_ref, *args, **kwargs):
    '''
    Execute the given function reference on ALL the workers in the given
    worker pool and return the return data from each.

    Pass in the arguments for the function, keep in mind that the sub needs
    to be loaded into the workers for a function to be available via
    hub.proc.run.add_sub
    '''
    workers = hub.proc.Workers[worker_name]
    ret = {}
    for ind in workers:
        payload = {'fun': 'run', 'ref': func_ref, 'args': args, 'kwargs': kwargs}
        # TODO: Make these futures to the run at the same time
        ret[ind] = await hub.proc.run.send(workers[ind], payload)
    return ret


async def func(hub, worker_name, func_ref, *args, **kwargs):
    '''
    Execute the given function reference on one worker in the given worker
    pool and return the return data.

    Pass in the arguments for the function, keep in mind that the sub needs
    to be loaded into the workers for a function to be available via
    hub.proc.run.add_sub
    '''
    workers = hub.proc.Workers[worker_name]
    w_iter = hub.proc.WorkersIter[worker_name]
    worker = workers[next(w_iter)]
    payload = {'fun': 'run', 'ref': func_ref, 'args': args, 'kwargs': kwargs}
    return await hub.proc.run.send(worker, payload)


async def send(hub, worker, payload):
    '''
    Send the given payload to the given worker. pass in the worker dict
    as derived from the pool (workers[ind])
    '''
    mp = msgpack.dumps(payload, use_bin_type=True)
    mp += hub.proc.DELIM
    reader, writer = await asyncio.open_unix_connection(path=worker['path'])
    writer.write(mp)
    await writer.drain()
    ret = await reader.readuntil(hub.proc.DELIM)
    ret = ret[:-len(hub.proc.DELIM)]
    writer.close()
    return msgpack.loads(ret, encoding='utf8')
