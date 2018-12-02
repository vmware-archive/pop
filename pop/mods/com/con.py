'''
Set up and manage the network connections
'''
# Import python libs
import asyncio
import os
import types

# Import third party libs
import aiohttp
import aiohttp.web
import msgpack




async def client(hub, pool_name, cname, addr, port, router):
    '''
    Creates a client connection to a remote server
    '''
    tgt = f'http://{addr}:{port}/ws'
    session = aiohttp.ClientSession()
    ws = await session.ws_connect(tgt)
    send_future = asyncio.ensure_future(hub.com.con.sender(ws, pool_name, cname))
    # release the loop so the future can run
    await asyncio.sleep(0.1)
    futures = []
    async for msg in ws:
        if msg.type == aiohttp.WSMsgType.BINARY:
            data = msgpack.loads(msg.data, raw=False)
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
        elif msg.type == aiohttp.WSMsgType.CLOSED:
            print('Session closed from remote')
            break
        elif msg.type == aiohttp.WSMsgType.ERROR:
            print('remote error')
            break
        for future in futures:
            if future.done():
                await future
    await send_future
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
    ws = aiohttp.web.WebSocketResponse()
    await ws.prepare(request)
    que = asyncio.Queue()
    pool_name = request.app['pool_name']
    router = request.app['router']
    r_str = os.urandom(4).hex()
    cname = f'{request.host}|{r_str}'
    hub.com.POOLS[pool_name]['cons'][cname] = {'que': que}
    send_future = asyncio.ensure_future(hub.com.con.sender(ws, pool_name, cname))
    futures = []
    await asyncio.sleep(0.01)
    async for msg in ws:
        if msg.type == aiohttp.WSMsgType.BINARY:
            data = msgpack.loads(msg.data, raw=False)
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
        elif msg.type == aiohttp.WSMsgType.CLOSED:
            print('Session closed from remote')
            break
        elif msg.type == aiohttp.WSMsgType.ERROR:
            print('remote error')
            break
        for future in futures:
            if future.done():
                await future
    que.put({'msg': 'BREAK'})
    await send_future
    await ws.close()


async def bind(hub, pool_name, addr, port, router):
    '''
    Binds to a local port and listens
    '''
    app = aiohttp.web.Application(debug=True)
    app['router'] = router
    app['pool_name'] = pool_name
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
    event = asyncio.Event()
    hub.com.EVENTS[data['stag']] = event
    await hub.com.POOLS[pool_name]['cons'][cname]['que'].put(data)
    while True:
        await event.wait()
        event.clear()
        ret = hub.com.RET.pop(data['stag'])
        yield ret['msg']
        if ret.get('done'):
            return


async def send_ret(hub, pool_name, cname, msg, rtag, done=True):
    '''
    Send a return
    '''
    data = {'msg': msg, 'done': done, 'rtag': rtag}
    await hub.com.POOLS[pool_name]['cons'][cname]['que'].put(data)
