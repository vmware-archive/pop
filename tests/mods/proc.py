# Import python libs
import random


async def callback(hub, payload):
    if 'payload' in payload:
        hub.set_me = payload['payload']['ret']
    return 'foo'


async def ret(hub):
    await hub.proc.worker.ret({'ret': 'Returned'})
    return 'inline'


async def gen(hub, start, end):
    for x in range(start, end):
        yield x


def simple_gen(hub, start, end):
    for x in range(start, end):
        yield x


def init_lasts(hub):
    hub.LASTS = {}
    return True


def echo_last(hub):
    '''
    Return 2 numbers, the second number is new, the first number is the same that
    was the second number the last time it was called
    '''
    try:
        next_ = random.randint(0, 50000)
        if 'last' not in hub.LASTS:
            hub.LASTS['last'] = 0
        last = hub.LASTS['last']
        hub.LASTS['last'] = next_
        return last, next_
    except Exception as exc:
        return 0, exc