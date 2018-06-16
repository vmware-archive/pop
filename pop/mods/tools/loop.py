# -*- coding: utf-8 -*-
'''
The main interface for management of the aio loop
'''
# Import python libs
import asyncio
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
    to be called after the creation fo the loop
    '''
    fun = hub.tools.ref.get_func(ref)
    asyncio.ensure_future(fun(*args, **kwargs))


def start(hub, *coros, hold=False):
    '''
    Start a loop that will run until complete
    '''
    hub.tools.loop.create()
    if hold:
        coros = list(coros)
        coros.append(_holder())
    # DO NOT CHANGE THIS CALL TO run_forever! If we do that then the tracebacks
    # do not get resolved.
    return hub.tools.Loop.run_until_complete(
            asyncio.gather(*coros)
            )


async def _holder():
    '''
    Just a sleeping while loop to hold the loop open while it runs until
    complete
    '''
    while True:
        await asyncio.sleep(60)


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
