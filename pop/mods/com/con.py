'''
Set up and manage the network connections
'''
# Import python libs
import asyncio
import os
import types
import random
import time

# Import third party libs
import aiohttp
import aiohttp.web
import msgpack


async def client(hub, pool_name, cname, addr, port, router, meta=None):
    '''
    Creates a client connection to a remote server and keeps the
    connection alive if the server goes down
    '''
    meta = {} if meta is None else meta
    while True:
        start = time.time()
        await _client(hub, pool_name, cname, addr, port, router, meta)
        end = time.time()
        if end - start < 1:
            # TODO: Make this configurable
            await asyncio.sleep(random.randrange(2, 20))


async def _client(hub, pool_name, cname, addr, port, router, meta):
    '''
    Creates a client connection to a remote server
    '''
    tgt = f'http://{addr}:{port}/ws'
    session = aiohttp.ClientSession()
    try:
        async with session.ws_connect(tgt) as ws:
            hub.tools.loop.ensure_future(
                'com.con.sender',
                ws,
                pool_name,
                cname)
            # release the loop so the future can run
            await asyncio.sleep(0)
            # send the initial metadata
            if meta:
                msg = {'meta': meta}
                async for ret in hub.com.con.send(pool_name, cname, msg):
                    pass
            async for msg in ws:
                if msg.type == aiohttp.WSMsgType.BINARY:
                    data = msgpack.loads(msg.data, raw=False)
                    if 'meta' in data:
                        hub.com.POOLS[pool_name]['cons'][cname]['meta'] = data['meta']
                    # Data will either be a return or it will be an execution request
                    # If the data has a tag it is a return
                    if 'rtag' in data:
                        await hub.com.RET[data['rtag']].put(data)
                        continue
                    else:
                        hub.tools.loop.ensure_future(
                            'com.init.f_router',
                            router,
                            pool_name,
                            cname,
                            data)
                elif msg.type == aiohttp.WSMsgType.CLOSED:
                    print('Session closed from remote')
                    break
                elif msg.type == aiohttp.WSMsgType.ERROR:
                    print('remote error')
                    break
    except aiohttp.client_exceptions.ClientConnectorError:
        # Float back up to the recon sequence
        pass
    await session.close()


async def sender(hub, ws, pool_name, cname):
    '''
    '''
    while True:
        data = await hub.com.POOLS[pool_name]['cons'][cname]['que'].get()
        await ws.send_bytes(
                msgpack.dumps(data, use_bin_type=True)
                )


async def wsh(hub, request):
    '''
    '''
    ws = aiohttp.web.WebSocketResponse(heartbeat=5)
    await ws.prepare(request)
    que = asyncio.Queue()
    pool_name = request.app['pool_name']
    router = request.app['router']
    meta = request.app['meta']
    r_str = os.urandom(4).hex()
    cname = f'{request.host}|{r_str}'
    hub.com.POOLS[pool_name]['cons'][cname] = {'que': que}
    hub.tools.loop.ensure_future('com.con.sender', ws, pool_name, cname)
    await asyncio.sleep(0)
    # send the initial metadata
    if meta:
        msg = {'meta': meta}
        async for ret in hub.com.con.send(pool_name, cname, msg):
            pass
    async for msg in ws:
        if msg.type == aiohttp.WSMsgType.BINARY:
            data = msgpack.loads(msg.data, raw=False)
            # If metadata is in the message, then update the metadata
            if 'meta' in data:
                hub.com.POOLS[pool_name]['cons'][cname]['meta'] = data['meta']
            # Data will either be a return or it will be an execution request
            # If the data has a tag it is a return
            if 'rtag' in data:
                await hub.com.RET[data['rtag']].put(data)
                continue
            else:
                hub.tools.loop.ensure_future(
                    'com.init.f_router',
                    router,
                    pool_name,
                    cname,
                    data)
        elif msg.type == aiohttp.WSMsgType.CLOSED:
            print('Session closed from remote')
            break
        elif msg.type == aiohttp.WSMsgType.ERROR:
            print('remote error')
            break
    que.put({'msg': 'BREAK'})
    await ws.close()
    hub.com.POOLS[pool_name]['cons'].pop(cname)
    del(que)


async def bind(hub, pool_name, addr, port, router, meta=None):
    '''
    Binds to a local port and listens
    '''
    app = aiohttp.web.Application(debug=True)
    app['router'] = router
    app['pool_name'] = pool_name
    app['meta'] = {} if meta is None else meta
    app.router.add_route('GET', '/ws', hub.com.con.wsh)
    runner = aiohttp.web.AppRunner(app)
    await runner.setup()
    site = aiohttp.web.TCPSite(runner, addr, port)
    await site.start()


async def send(hub, pool_name, cname, msg, done=True):
    '''
    Sends the message by placing it on the router que and waiting for it
    to be completed
    '''
    data = {'msg': msg, 'done': done}
    data['stag'] = os.urandom(16)
    hub.com.RET[data['stag']] = asyncio.Queue()
    await hub.com.POOLS[pool_name]['cons'][cname]['que'].put(data)
    count = 0
    dcount = -1
    while True:
        count += 1
        ret = await hub.com.RET[data['stag']].get()
        if not ret.get('eof'):
            yield ret['msg']
        if ret.get('done'):
            dcount = ret['count']
        if dcount == count:
            return


async def send_ret(hub, pool_name, cname, msg, rtag, done=True, count=1, eof=False):
    '''
    Send a return
    '''
    data = {'msg': msg, 'done': done, 'rtag': rtag, 'count': count}
    if eof:
        data['eof'] = True
    await hub.com.POOLS[pool_name]['cons'][cname]['que'].put(data)
