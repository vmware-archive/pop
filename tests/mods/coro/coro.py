# -*- coding: utf-8 -*-

__virtualname__ = 'coro'

# Import python libs
import asyncio

# Import third party libs
try:
    import tornado.gen
    HAS_TORNADO = True
except ImportError:
    HAS_TORNADO = False


@asyncio.coroutine
def asyncio_demo():
    return True


if HAS_TORNADO:
    @tornado.gen.coroutine
    def tornado_demo(hub):
        return False
