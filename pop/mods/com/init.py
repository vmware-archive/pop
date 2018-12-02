'''
Set up the dflow system on the hub
'''
# Import python libs
import os
import types
import asyncio


def new(hub):
    '''
    Set up the keys and structures used by dflow
    '''
    hub.com.POOLS = {}
    hub.com.RET = {}
    hub.com.EVENTS = {}
    hub.com.DELIM = b'd\xff\xcfCO)\xfe='


async def f_router(hub, router, pool_name, cname, data):
    ctx = {'pool_name': pool_name, 'cname': cname, 'data': data}
    if 'stag' in data:
        rtag = data['stag']
    else:
        rtag = None
    ret = router(ctx, data['msg'])
    if isinstance(ret, types.AsyncGeneratorType):
        async for rmsg in ret:
            await hub.com.con.send_ret(pool_name, cname, rmsg, rtag, done=False)
        await hub.com.con.send_ret(pool_name, cname, {}, rtag, done=True)
    elif isinstance(ret, types.GeneratorType):
        for rmsg in ret:
            await hub.com.con.send_ret(pool_name, cname, rmsg, rtag, done=False)
        await hub.com.con.send_ret(pool_name, cname, {}, rtag, done=True)
    elif asyncio.iscoroutine(ret):
        rmsg = await ret
        await hub.com.con.send_ret(pool_name, cname, rmsg, rtag)


async def as_yielded(hub, gens):
    '''
    Concurrently run multiple async generators and yield the next yielded
    value from the soonest yielded generator.

    async def many():
        for n in range(10):
            yield os.urandom(6).hex()

    async def run():
        gens = []
        for n in range(10):
            gens.append(many())
        async for y in as_yielded(gens):
            print(y)
    '''
    fin = os.urandom(32)
    que = asyncio.Queue()
    fs = []
    to_clean = []
    async def _yield(gen):
        async for comp in gen:
            await que.put(comp)
    async def _ensure(coros):
        for f in asyncio.as_completed(coros):
            await f
    async def _set_done():
        await que.put(fin)
    def _done(future):
        to_clean.append(asyncio.ensure_future(_set_done()))
    coros = []
    for gen in gens:
        coros.append(_yield(gen))
    f = asyncio.ensure_future(_ensure(coros))
    f.add_done_callback(_done)
    while True:
        ret = await que.get()
        if ret == fin:
            break
        yield ret
    for c in to_clean:
        await c
