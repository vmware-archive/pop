# -*- coding: utf-8 -*-
'''
The main interface for management of the aio loop
'''
# Import python libs
import asyncio
import functools

__virtualname__ = 'loop'


def __virtual__(hub):
    return True


def create(hub):
    '''
    Create the loop at hub.loop.loop
    '''
    if not hasattr(hub.tools, '_loop'):
        hub.tools._loop = asyncio.get_event_loop()


def call_soon(hub, trine, *args, **kwargs):
    '''
    Schedule a coroutine to be called when the loop has time. This needs
    to be called after the creation fo the loop
    '''
    fun = hub.tools.trine.get_func(trine)
    hub.tools._loop.call_soon(functools.partial(fun, *args, **kwargs))


def ensure_future(hub, trine, *args, **kwargs):
    '''
    Schedule a coroutine to be called when the loop has time. This needs
    to be called after the creation fo the loop
    '''
    fun = hub.tools.trine.get_func(trine)
    asyncio.ensure_future(fun(*args, **kwargs))


def entry(hub):
    '''
    The entry coroutine to start a run forever loop

    This is meant to be called once and sets up the loop on the hub as
    hub.loop.loop
    '''
    hub.tools._loop.run_forever()


def start(hub, trine, *args, **kwargs):
    '''
    Start a loop that will run until complete
    '''
    fun = hub.tools.trine.get_func(trine)
    hub.tools.loop.create()
    return hub.tools._loop.run_until_complete(
            asyncio.gather(fun(*args, **kwargs))
            )


@asyncio.coroutine
def kill(hub, wait=0):
    '''
    Close out the loop
    '''
    yield from asyncio.sleep(wait)
    hub.tools._loop.stop()
    while True:
        if not hub.tools._loop.is_running():
            hub.tools._loop.close()
        yield from asyncio.sleep(1)
