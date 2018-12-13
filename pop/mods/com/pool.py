'''
Manage multiple connection pools
'''
# Import python libs
import os
import asyncio
import random
import collections


def create(hub, pool_name, router):
    '''
    Create a named connection pool
    '''
    if pool_name not in hub.com.POOLS:
        hub.com.POOLS[pool_name] = {
                'cons': {},
                'router': router}
        return
    raise KeyError('Pool named "{}" already exists'.format(pool_name))


async def add_unix_con(hub, pool_name, con_type, path):
    '''
    Add a unix socket connection to a named pool.

    YES! You can have a pool with websocket connections and socket
    connections, once they are in a pool they all behave the same way!
    '''
    cname = os.urandom(8)
    if cname in hub.com.POOLS:
        raise KeyError(f'Connection {cname} already exists')
    router = hub.com.POOLS[pool_name]['router']
    que = asyncio.Queue()
    if con_type == 'client':
        hub.com.POOLS[pool_name]['cons'][cname] = {'que': que}
        hub.tools.loop.ensure_future(
            'com.unix.client',
            pool_name,
            cname,
            path,
            router)
    elif con_type == 'bind':
        hub.tools.loop.ensure_future(
            'com.unix.bind',
            pool_name,
            path,
            router)


async def add_con(hub, pool_name, con_type, addr, port, proto='ipv4', meta=None):
    '''
    Add a connection to the pool that will connect to a remote port and
    listen for inbound data
    '''
    r_str = os.urandom(4).hex()
    cname = f'{addr}:{port}|{r_str}'
    if cname in hub.com.POOLS:
        raise KeyError(f'Connection {cname} already exists')
    router = hub.com.POOLS[pool_name]['router']
    que = asyncio.Queue()
    if con_type == 'client':
        hub.com.POOLS[pool_name]['cons'][cname] = {'que': que}
        hub.tools.loop.ensure_future(
            'com.con.client',
            pool_name,
            cname,
            addr,
            port,
            router)
    elif con_type == 'bind':
        hub.tools.loop.ensure_future(
            'com.con.bind',
            pool_name,
            addr,
            port,
            router)


async def pub(hub, pool_name, msg):
    '''
    Publish the message to all membbers of the named pool
    '''
    gens = []
    for cname in hub.com.POOLS[pool_name]['cons']:
        gen = hub.com.con.send(pool_name, cname, msg)
        gens.append(gen)
    async for ret in hub.com.init.as_yielded(gens):
        yield ret


async def rand(hub, pool_name, msg):
    '''
    Randomly select a member of the pool to send a message out
    '''
    cname = random.choice(list(hub.com.POOLS[pool_name]['cons']))
    async for ret in hub.com.con.send(pool_name, cname, msg):
        yield ret


async def avail(hub, pool_name, msg):
    '''
    Send the message to the first connection to pick it up, or the most
    available connection.
    This is done by looking at the queues in the pipe for each connection
    and selecting the connection with the smallest length queue.
    '''
    best = {}
    for cname, data in hub.com.POOLS[pool_name]['cons'].items():
        if not best:
            best = {'cname': cname, 'len': data['que'].qsize()}
            continue
        if best['len'] == 0:
            break
        qlen = data['que'].qsize()
        if qlen < best['len']:
            best = {'cname': cname, 'len': data['que'].qsize()}
    cname = best['cname']
    async for ret in hub.com.con.send(pool_name, cname, msg):
        yield ret