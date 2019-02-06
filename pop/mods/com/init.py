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
    hub.tools.sub.add('tgt', pypath='pop.mods.tgt')
    hub.com.POOLS = {}
    hub.com.RET = {}
    hub.com.DELIM = b'd\xff\xcfCO)\xfe='


async def f_router(hub, router, pool_name, cname, data):
    ctx = {'pool_name': pool_name, 'cname': cname, 'data': data}
    if 'stag' in data:
        rtag = data['stag']
    else:
        rtag = None
    ret = router(ctx, data['msg'])
    if isinstance(ret, types.AsyncGeneratorType):
        count = 0
        async for rmsg in ret:
            count += 1
            await hub.com.con.send_ret(pool_name, cname, rmsg, rtag, done=False, count=count)
        count += 1
        await hub.com.con.send_ret(pool_name, cname, '', rtag, done=True, count=count, eof=True)
    elif isinstance(ret, types.GeneratorType):
        count = 0
        for rmsg in ret:
            count += 1
            await hub.com.con.send_ret(pool_name, cname, rmsg, rtag, done=False, count=count)
        count += 1
        await hub.com.con.send_ret(pool_name, cname, '', rtag, done=True, count=count, eof=True)
    elif asyncio.iscoroutine(ret):
        rmsg = await ret
        await hub.com.con.send_ret(pool_name, cname, rmsg, rtag)