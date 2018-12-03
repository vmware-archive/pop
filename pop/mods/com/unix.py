# Import python libs
import asyncio
import os
# Import third party libs
import msgpack


async def client(hub, pool_name, cname, path, router):
    '''
    Create a unix socket client creation to the given path
    '''
    reader, writer = await asyncio.open_unix_connection(path)
    send_future = asyncio.ensure_future(hub.com.unix.sender(writer, pool_name, cname))
    # release the loop so the future can run
    await asyncio.sleep(0.01)
    futures = []
    while True:
        msg = await reader.readuntil(hub.com.DELIM)
        data = msg[:-len(hub.com.DELIM)]
        data = msgpack.loads(data, raw=False)
        # Data will either be a return or it will be an execution request
        # If the data has a tag it is a return
        if 'rtag' in data:
            hub.com.RET[data['rtag']] = data
            hub.com.EVENTS[data['rtag']].set()
            continue
        else:
            futures.append(
                asyncio.ensure_future(
                    hub.com.init.f_router(
                        router,
                        pool_name,
                        cname,
                        data)))
        for future in futures:
            if future.done():
                await future
    await send_future


async def bind(hub, pool_name, path, router):
    '''
    Start a local unix socket communication interface
    '''
    worker = await hub.com.unix.gen_worker(pool_name, path, router)
    await asyncio.start_unix_server(
        worker,
        path)


async def sender(hub, writer, pool_name, cname):
    '''
    Stand up a unix socket sender coroutine that will wait for messages
    to be put on the connection que and then send them
    '''
    while True:
        data = await hub.com.POOLS[pool_name]['cons'][cname]['que'].get()
        snd = msgpack.dumps(data, use_bin_type=True)
        snd += hub.com.DELIM
        writer.write(snd)
        await writer.drain()


async def gen_worker(hub, pool_name, path, router):
    '''
    Return a closure function that is used to generate the connections
    as the come in for a unix socket server
    '''
    async def worker(reader, writer):
        cname = os.urandom(8)
        que = asyncio.Queue()
        hub.com.POOLS[pool_name]['cons'][cname] = {'que': que}
        send_future = asyncio.ensure_future(hub.com.unix.sender(writer, pool_name, cname))
        await asyncio.sleep(0.01)
        futures = []
        while True:
            msg = await reader.readuntil(hub.com.DELIM)
            data = msg[:-len(hub.com.DELIM)]
            data = msgpack.loads(data, raw=False)
            # Data will either be a return or it will be an execution request
            # If the data has a tag it is a return
            if 'rtag' in data:
                hub.com.RET[data['rtag']] = data
                hub.com.EVENTS[data['rtag']].set()
                continue
            else:
                futures.append(
                    asyncio.ensure_future(
                        hub.com.init.f_router(
                            router,
                            pool_name,
                            cname,
                            data)))
            for future in futures:
                if future.done():
                    await future
    return worker
