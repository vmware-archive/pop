# -*- coding: utf-8 -*-
'''
The main interface for management of the aio loop
'''
# Import python libs
import asyncio
import os
import sys
import functools

__virtualname__ = 'loop'


def __virtual__(hub):
    return True


def create(hub):
    '''
    Create the loop at hub.tools.Loop
    '''
    if not hub.tools.Loop:
        hub.tools.loop.FUT_QUE = asyncio.Queue()
        if sys.platform == 'win32':
            hub.tools.Loop = asyncio.ProactorEventLoop()
        else:
            hub.tools.Loop = asyncio.get_event_loop()


def call_soon(hub, ref, *args, **kwargs):
    '''
    Schedule a coroutine to be called when the loop has time. This needs
    to be called after the creation fo the loop
    '''
    fun = hub.tools.ref.get_func(ref)
    hub.tools.Loop.call_soon(functools.partial(fun, *args, **kwargs))


def ensure_future(hub, ref, *args, **kwargs):
    '''
    Schedule a coroutine to be called when the loop has time. This needs
    to be called after the creation fo the loop. This function also uses
    the hold system to await the future when it is done making it easy
    to create a future that will be cleanly awaited in the background.
    '''
    fun = hub.tools.ref.last(ref)
    future = asyncio.ensure_future(fun(*args, **kwargs))

    def callback(fut):
        hub.tools.loop.FUT_QUE.put_nowait(fut)
    future.add_done_callback(callback)


def start(hub, *coros, hold=False):
    '''
    Start a loop that will run until complete
    '''
    hub.tools.loop.create()
    if hold:
        coros = list(coros)
        coros.append(_holder(hub))
    # DO NOT CHANGE THIS CALL TO run_forever! If we do that then the tracebacks
    # do not get resolved.
    return hub.tools.Loop.run_until_complete(
            asyncio.gather(*coros)
            )


async def _holder(hub):
    '''
    Just a sleeping while loop to hold the loop open while it runs until
    complete
    '''
    while True:
        future = await hub.tools.loop.FUT_QUE.get()
        await future


async def await_futures(hub):
    '''
    Scan over the futures that have completed and manually await them.
    This function is used to clean up futures when the loop is not opened
    up with hold=True so that ensured futures can be cleaned up on demand
    '''
    while not hub.tools.loop.FUT_QUE.empty():
        future = await hub.tools.loop.FUT_QUE.get()
        await future


async def kill(hub, wait=0):
    '''
    Close out the loop
    '''
    await asyncio.sleep(wait)
    hub.tools.Loop.stop()
    while True:
        if not hub.tools.Loop.is_running():
            hub.tools.Loop.close()
        await asyncio.sleep(1)


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
